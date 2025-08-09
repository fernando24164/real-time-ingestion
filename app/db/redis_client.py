import redis.asyncio as aioredis
from redis.exceptions import ConnectionError as RedisConnectionError

from app.core.config import settings


def connect_redis_pool() -> aioredis.ConnectionPool:
    try:
        return aioredis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=10)
    except RedisConnectionError as e:
        message = f"Failed to connect to Redis: {e}"
        raise RedisConnectionError(message) from e
