import os
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:dev@localhost:5432/metro"
)

engine = create_async_engine(DATABASE_URL, echo=True)