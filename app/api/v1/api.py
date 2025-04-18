from fastapi import APIRouter

from app.api.v1.endpoints import ingestion, last_games_view, user, customer_insights

api_router = APIRouter(prefix="/v1")

api_router.include_router(ingestion.ingestion_router)
api_router.include_router(last_games_view.last_viewed_router)
api_router.include_router(user.user_router)
api_router.include_router(customer_insights.insights_router)
