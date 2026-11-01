# ad-service

FastAPI service for managing ads and users.

## Stack

- FastAPI, SQLAlchemy (async), Pydantic
- PostgreSQL
- Alembic migrations
- Docker / docker-compose

## Quick start

```bash
cp .env.example .env  # or edit .env
docker compose up -d --build
```

API: http://localhost:8000/docs

## Local development

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn ad_service.main:app --reload
```

## Tests

```bash
uv run pytest
```

