from fastapi.background import BackgroundTasks
from fastapi.routing import APIRouter

from app.api.deps import DBSessionDep, RedisConnectionDep
from app.schemas.ingestion import IngestionSchema
from app.services.ingestion_service import ingest_data_service

ingestion_router = APIRouter(tags=["Ingestion"])


@ingestion_router.post("/ingest", response_model=dict)
async def ingest_data(
    data: IngestionSchema,
    background_tasks: BackgroundTasks,
    redis_client: RedisConnectionDep,
    postgres_session: DBSessionDep,
) -> dict:
    background_tasks.add_task(ingest_data_service, data, redis_client, postgres_session)
    return {"message": "Data ingested successfully"}
