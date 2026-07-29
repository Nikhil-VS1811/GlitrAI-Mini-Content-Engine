"""Health-check endpoints."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter(tags=["health"])


@router.get("/health", response_model=None)
def health_check(
    db: Session = Depends(get_db),
) -> dict[str, str] | JSONResponse:
    """Confirm that the API can establish a PostgreSQL connection."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": "disconnected"},
        )

    return {"status": "healthy", "database": "connected"}
