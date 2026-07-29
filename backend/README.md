# Mini Content Engine — Backend

Production-oriented FastAPI scaffold for an AI-powered content engine. This initial version intentionally contains no content-generation or domain business logic.

## Project layout

- `app/main.py` creates the FastAPI application and provides `GET /health`.
- `app/config.py` loads `.env` values into the immutable `settings` object.
- `app/database.py` configures the SQLAlchemy engine, session factory, and base class for future models.
- `app/models.py` is reserved for SQLAlchemy models.
- `app/schemas.py` is reserved for Pydantic request and response schemas.
- `app/routes/` will hold API routers grouped by feature.
- `app/services/` will hold business/application services.
- `app/utils/` will hold reusable helpers.
- `app/uploads/` is reserved for uploaded assets.
- `app/generated/` is reserved for generated content artifacts.
- `requirements.txt` lists the application dependencies.
- `.env.example` documents the required environment variables.

## Run locally

1. Create and activate a Python 3.12 virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and update `DATABASE_URL` for your PostgreSQL instance.
4. Start the API: `uvicorn app.main:app --reload`.

Then open `http://127.0.0.1:8000/health`; it returns `{"status":"ok"}`.
