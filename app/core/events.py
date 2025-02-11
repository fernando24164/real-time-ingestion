from fastapi import FastAPI

from app.db.opensearch_client import connect_opensearch
from app.db.redis_client import connect_redis_pool


def startup_db_clients(app: FastAPI) -> None:
    opensearch_client = connect_opensearch()
    app.state.opensearch_client = opensearch_client

    redis_pool = connect_redis_pool()
    app.state.redis_pool = redis_pool


async def shutdown_db_clients(app: FastAPI) -> None:
    if app.state.opensearch_client:
        await app.state.opensearch_client.close()
    if app.state.redis_pool:
        await app.state.redis_pool.disconnect()
