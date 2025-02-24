from app.schemas.ingestion import IngestionSchema
from opensearchpy._async.client import AsyncOpenSearch
import redis.asyncio as redis


async def ingest_data_service(
    data: IngestionSchema, opensearch_client: AsyncOpenSearch, redis_client: redis.Redis
) -> None:
    await opensearch_client.index(
        index="ingestion", body=data.model_dump(), refresh=True
    )

    pipeline = redis_client.pipeline()
    pipeline.rpush(f"last_viewed:{data.customer_id}", data.product_id)
    pipeline.ltrim(f"last_viewed:{data.customer_id}", 0, 9)
    await pipeline.execute()
