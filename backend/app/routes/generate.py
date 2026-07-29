"""Endpoints for accepting content-generation requests."""
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import JobCreateResponse
from app.services.job_service import create_job, process_marketing_prompt_job


router = APIRouter(tags=["generation"])
UPLOAD_DIRECTORY = Path(__file__).resolve().parents[1] / "uploads"
CHUNK_SIZE = 1024 * 1024
IMAGE_EXTENSIONS = {
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


async def _save_upload(image: UploadFile, destination: Path) -> None:
    """Stream an uploaded image to local storage without loading it all into memory."""
    try:
        with destination.open("wb") as output_file:
            while chunk := await image.read(CHUNK_SIZE):
                output_file.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await image.close()


@router.post("/generate", response_model=JobCreateResponse, status_code=status.HTTP_201_CREATED)
async def generate(
    background_tasks: BackgroundTasks,
    product_name: str = Form(..., min_length=1, max_length=255),
    description: str = Form(..., min_length=1),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> JobCreateResponse:
    """Store a pending job and its source image for later processing."""
    extension = IMAGE_EXTENSIONS.get(image.content_type or "")
    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file.",
        )

    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4()}{extension}"
    destination = UPLOAD_DIRECTORY / filename

    try:
        await _save_upload(image, destination)
        job = create_job(
            db,
            product_name=product_name,
            description=description,
            uploaded_image=filename,
        )
        background_tasks.add_task(process_marketing_prompt_job, job.id)
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create job.",
        ) from exc

    return JobCreateResponse(job_id=job.id, status=job.status)
