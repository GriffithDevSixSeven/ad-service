"""FastAPI application entrypoint."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ad_service.core.exceptions import AppError, NotFoundError
from ad_service.database import Base, engine
from ad_service.routers import ads_router, auth_router, users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ad-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="ad-service", lifespan=lifespan)
app.include_router(ads_router)
app.include_router(auth_router)
app.include_router(users_router)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc) or "Not found"})


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
