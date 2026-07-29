"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    """Read a conventional boolean environment variable."""
    return getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the API."""

    app_name: str = getenv("APP_NAME", "Mini Content Engine")
    debug: bool = _get_bool("DEBUG")
    database_url: str = getenv(
        "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/content_engine"
    )


settings = Settings()
