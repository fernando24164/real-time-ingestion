from fastapi import status, Body
from uuid import uuid4

from fastapi.background import BackgroundTasks
from fastapi.routing import APIRouter
from loguru import logger

from app.api.deps import DBSessionDep, RedisConnectionDep
from app.schemas.ingestion import IngestionResponse, IngestionSchema
from app.services.ingestion_service import ingest_data_service

ingestion_router = APIRouter(tags=["Ingestion"])


@ingestion_router.post(
    "/ingest",
    response_model=IngestionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Data ingestion request accepted"},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"description": "Payload too large"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid input data"},
    },
)
async def ingest_data(
    background_tasks: BackgroundTasks,
    redis_client: RedisConnectionDep,
    postgres_session: DBSessionDep,
    data: IngestionSchema = Body(..., max_size=1024 * 1024),  # 1MB limit
) -> IngestionResponse:
    """
    Ingest user activity data.

    This endpoint queues the data for processing in a background task.
    The response is immediate while processing continues asynchronously.

    Args:
        data: The user activity data to ingest
        background_tasks: FastAPI background tasks handler
        redis_client: Redis connection for caching recent views
        postgres_session: Database session for persistent storage

    Returns:
        IngestionResponse: A response indicating the request was accepted
    """

    async def wrapped_ingestion_task(data, redis_client, postgres_session):
        try:
            await ingest_data_service(data, redis_client, postgres_session)
        except Exception as e:
            logger.exception(f"Error ingesting data: {e}")

    background_tasks.add_task(
        wrapped_ingestion_task, data, redis_client, postgres_session
    )
    return IngestionResponse(
        status="accepted",
        message="Data ingestion successfully queued",
        request_id=uuid4(),
    )