from fastapi import FastAPI

from app.db.postgres_pool import create_engine_pg, create_session_factory
from app.db.redis_client import connect_redis_pool


async def startup_db_clients(app: FastAPI) -> None:
    redis_pool = connect_redis_pool()
    app.state.redis_pool = redis_pool

    engine = create_engine_pg()
    app.state.engine_pg = engine

    session_factory = create_session_factory(engine)
    app.state.session_factory = session_factory


async def shutdown_db_clients(app: FastAPI) -> None:
    if app.state.redis_pool:
        await app.state.redis_pool.disconnect()
    if app.state.engine_pg:
        await app.state.engine_pg.dispose()
