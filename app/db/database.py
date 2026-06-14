from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
async_session_local = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_local() as session:
        yield session
