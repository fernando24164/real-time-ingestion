from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Request
from opensearchpy._async.client import AsyncOpenSearch


def get_async_opensearch_client(request: Request):
    return request.app.state.opensearch_client


def get_redis_connection(request: Request):
    return redis.Redis.from_pool(request.app.state.redis_pool)


OpenSearchClientDep = Annotated[AsyncOpenSearch, Depends(get_async_opensearch_client)]
RedisConnectionDep = Annotated[redis.Redis, Depends(get_redis_connection)]
