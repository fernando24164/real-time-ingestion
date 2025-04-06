import redis.asyncio as redis
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.web_event import WebEvents
from app.schemas.ingestion import IngestionSchema


async def ingest_data_service(
    data: IngestionSchema, redis_client: redis.Redis, postgres_session: AsyncSession
) -> None:
    try:
        if data.product_id:
            pipeline = redis_client.pipeline()
            pipeline.rpush(f"last_viewed:{data.customer_id}", data.product_id)
            pipeline.ltrim(f"last_viewed:{data.customer_id}", 0, 9)
            await pipeline.execute()

        web_event = WebEvents(**data.model_dump())
        postgres_session.add(web_event)
        await postgres_session.commit()
    except Exception as e:
        logger.exception(f"Error ingesting data: {e}")
        raise
