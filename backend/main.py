from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from backend.config import settings
from backend.database import engine

from backend.models import Base

from backend.routers import TodoRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(
    TodoRouter,
)
