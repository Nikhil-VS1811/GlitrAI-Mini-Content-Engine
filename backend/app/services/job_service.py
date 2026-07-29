"""Persistence and processing workflow for content-generation jobs."""

import logging
from pathlib import Path
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.enums import JobStatus
from app.models import Job
from app.services.image_service import generate_image
from app.services.ollama_service import generate_marketing_prompt


logger = logging.getLogger(__name__)


class JobNotFoundError(LookupError):
    """Raised when a requested job does not exist."""


def create_job(
    db: Session,
    *,
    product_name: str,
    description: str,
    uploaded_image: str,
) -> Job:
    """Create and persist a job in its initial pending state."""
    job = Job(
        product_name=product_name,
        description=description,
        uploaded_image=uploaded_image,
        status=JobStatus.PENDING,
    )
    try:
        db.add(job)
        db.commit()
        db.refresh(job)
    except SQLAlchemyError:
        db.rollback()
        raise

    return job


def get_job(db: Session, job_id: UUID) -> Job:
    """Fetch a job or raise a domain-specific not-found error."""
    job = db.get(Job, job_id)
    if job is None:
        raise JobNotFoundError(f"Job {job_id} was not found.")
    return job


def _commit_and_refresh(db: Session, job: Job) -> Job:
    """Commit a job mutation and restore a reusable session on failure."""
    try:
        db.commit()
        db.refresh(job)
    except SQLAlchemyError:
        db.rollback()
        raise
    return job


def mark_job_processing(db: Session, job_id: UUID) -> Job:
    """Move a job into processing before contacting the generation provider."""
    job = get_job(db, job_id)
    job.status = JobStatus.PROCESSING
    return _commit_and_refresh(db, job)


def complete_job(
    db: Session,
    job_id: UUID,
    generated_prompt: str,
    generated_image: str,
) -> Job:
    """Store generated outputs and mark a job as completed."""
    job = get_job(db, job_id)
    job.generated_prompt = generated_prompt
    job.generated_image = generated_image
    job.status = JobStatus.COMPLETED
    return _commit_and_refresh(db, job)


def fail_job(db: Session, job_id: UUID) -> Job:
    """Mark a job as failed after a processing error."""
    job = get_job(db, job_id)
    job.status = JobStatus.FAILED
    return _commit_and_refresh(db, job)


def process_marketing_prompt_job(job_id: UUID) -> None:
    """Run the prompt-generation lifecycle in a FastAPI background task."""
    db = SessionLocal()
    try:
        job = mark_job_processing(db, job_id)

        # Try Ollama first, fall back if unavailable
        try:
            generated_prompt = generate_marketing_prompt(
                job.product_name,
                job.description,
            )
        except Exception:
            logger.warning("Ollama unavailable. Using fallback prompt.")
            generated_prompt = (
                f"Professional studio product photograph of {job.product_name}. "
                f"{job.description}. Soft lighting, premium ecommerce style, "
                f"high quality, white background."
            )

        if job.uploaded_image is None:
            raise ValueError("Job has no uploaded image.")

        uploaded_image_path = str(
            Path(__file__).resolve().parents[1] / "uploads" / job.uploaded_image
        )

        generated_image = generate_image(
            generated_prompt,
            uploaded_image_path,
        )

        complete_job(
            db,
            job_id,
            generated_prompt,
            generated_image,
        )

    except Exception:
        logger.exception("Marketing prompt generation failed for job %s", job_id)
        try:
            fail_job(db, job_id)
        except (JobNotFoundError, SQLAlchemyError):
            logger.exception("Unable to mark job %s as failed", job_id)
    finally:
        db.close()
