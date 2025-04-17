from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.models.game_store import Base


def create_engine_pg(config=get_settings()) -> AsyncEngine:
    async_engine = create_async_engine(
        config.POSTGRES_DATABASE_URL,
        pool_size=config.PG_POOL_SIZE,
        max_overflow=config.PG_POOL_OVERFLOW,
    )
    return async_engine


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
