from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
print(engine.url)

# IMPORTANT: Import the model so SQLAlchemy registers it
from app.models import Job

from app.routes.generate import router as generate_router
from app.routes.health import router as health_router
from app.routes.jobs import router as jobs_router
print("Registered tables:", Base.metadata.tables.keys())
# Create all database tables
Base.metadata.create_all(bind=engine)
print("Finished create_all()")

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/generated",
    StaticFiles(directory=Path(__file__).resolve().parent / "generated"),
    name="generated",
)

app.include_router(health_router)
app.include_router(generate_router)
app.include_router(jobs_router)
