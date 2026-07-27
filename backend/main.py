from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from backend.config import settings
from backend.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    print('бд прогружено?')
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)
