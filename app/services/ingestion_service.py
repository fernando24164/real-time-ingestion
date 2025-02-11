from app.schemas.ingestion import IngestionSchema
from opensearchpy._async.client import AsyncOpenSearch
import redis.asyncio as redis


async def ingest_data_service(
    data: IngestionSchema, opensearch_client: AsyncOpenSearch, redis_client: redis.Redis
) -> None:
    await opensearch_client.index(
        index="ingestion", body=data.model_dump(), refresh=True
    )
    await redis_client.rpush(f"last_viewed:{data.customer_id}", data.product_id)
    await redis_client.ltrim(f"last_viewed:{data.customer_id}", -10, -1)
