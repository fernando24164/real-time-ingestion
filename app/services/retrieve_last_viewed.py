from io import BytesIO

import redis.asyncio as redis

from app.services.exceptions import NoLastViewed


async def get_last_viewed(
    customer_id: int, redis_client: redis.Redis, start: int = 0, stop: int = 9
) -> dict:
    products = await redis_client.lrange(f"last_viewed:{customer_id}", start, stop)
    if not products:
        raise NoLastViewed(f"No last viewed products found for the customer {customer_id}")

    return {"last_viewed_product": products.decode("utf-8")}
