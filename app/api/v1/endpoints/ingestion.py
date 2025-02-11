from fastapi.background import BackgroundTasks
from fastapi.routing import APIRouter

from app.api.deps import GetOpenSearchClient, GetRedisConnection
from app.schemas.ingestion import IngestionSchema
from app.services.ingestion_service import ingest_data_service

ingestion_router = APIRouter(tags=["Ingestion"])


@ingestion_router.post("/ingest", response_model=dict)
async def ingest_data(
    data: IngestionSchema,
    background_tasks: BackgroundTasks,
    opensearch_client: GetOpenSearchClient,
    redis_client: GetRedisConnection,
) -> dict:
    background_tasks.add_task(
        ingest_data_service, data, opensearch_client, redis_client
    )
    return {"message": "Data ingested successfully"}
