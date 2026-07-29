"""Pydantic schemas for the jobs domain."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums import JobStatus


class JobCreate(BaseModel):
    """Validated data required to create a new job."""

    product_name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    uploaded_image: str | None = Field(default=None, max_length=512)


class JobResponse(BaseModel):
    """Full job representation returned by future API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_name: str
    description: str
    uploaded_image: str | None
    generated_prompt: str | None
    generated_image: str | None
    status: JobStatus
    created_at: datetime
    updated_at: datetime


class JobStatusResponse(BaseModel):
    """Small response shape for job-status lookups."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: JobStatus
    updated_at: datetime


class JobCreateResponse(BaseModel):
    """Response returned after a job has been accepted for processing."""

    job_id: UUID
    status: JobStatus


class JobDetailResponse(BaseModel):
    """Generation state and outputs for a single job."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: JobStatus
    generated_prompt: str | None
    generated_image: str | None
    created_at: datetime
    updated_at: datetime
