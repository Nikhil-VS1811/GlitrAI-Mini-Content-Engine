"""SQLAlchemy engine and request-scoped session configuration."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker[Session](
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for future SQLAlchemy models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for one request and close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
