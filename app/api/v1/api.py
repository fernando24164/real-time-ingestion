from fastapi import APIRouter

from app.api.v1.endpoints import ingestion
from app.api.v1.endpoints import last_product_view

api_router = APIRouter(prefix="/v1")

api_router.include_router(ingestion.ingestion_router)
api_router.include_router(last_product_view.last_viewed_router)
