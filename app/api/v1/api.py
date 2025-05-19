from fastapi import APIRouter

from app.api.v1.endpoints import (
    customer_insights,
    game,
    genre,
    ingestion,
    publisher,
    session_insights,
    user,
)

api_router = APIRouter(prefix="/v1")

api_router.include_router(ingestion.ingestion_router)
api_router.include_router(user.user_router)
api_router.include_router(customer_insights.insights_router)
api_router.include_router(publisher.publisher_router)
api_router.include_router(genre.genre_router)
api_router.include_router(session_insights.session_router)
api_router.include_router(game.game_router)
