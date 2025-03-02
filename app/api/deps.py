from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


def get_redis_connection(request: Request):
    return redis.Redis.from_pool(request.app.state.redis_pool)


async def get_pg_connection(request: Request):
    async with request.app.state.session_factory() as session:
        return session


RedisConnectionDep = Annotated[redis.Redis, Depends(get_redis_connection)]
DBSessionDep = Annotated[AsyncSession, Depends(get_pg_connection)]
