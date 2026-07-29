"""Read-only endpoints for content-generation jobs."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import JobDetailResponse
from app.services.job_service import JobNotFoundError, get_job


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobDetailResponse)
def get_job_by_id(
    job_id: UUID,
    db: Session = Depends(get_db),
) -> JobDetailResponse:
    """Return the current generation result and lifecycle state for one job."""
    try:
        job = get_job(db, job_id)
    except JobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        ) from exc

    return JobDetailResponse.model_validate(job)
