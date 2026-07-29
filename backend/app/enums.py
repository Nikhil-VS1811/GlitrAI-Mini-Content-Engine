"""Shared application enumerations."""

from enum import StrEnum


class JobStatus(StrEnum):
    """Allowed lifecycle states for a content-generation job."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
