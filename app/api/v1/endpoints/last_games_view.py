from fastapi import APIRouter, HTTPException, Query

from app.api.deps import RedisConnectionDep
from app.services.exceptions import NoLastViewed
from app.services.retrieve_last_viewed import get_last_viewed
from app.schemas.last_viewed import LastViewedGamesResponse

last_viewed_router = APIRouter(tags=["Last viewed games"])


@last_viewed_router.get("/last_games_viewed", response_model=LastViewedGamesResponse)
async def last_games_view(
    redis_client: RedisConnectionDep,
    user_id: int = Query(..., description="User ID"),
) -> LastViewedGamesResponse:
    """
    Retrieve the last viewed games for a specific user.
    
    Returns a list of game IDs that were last viewed by the user.
    """
    try:
        games = await get_last_viewed(user_id, redis_client)
    except NoLastViewed as e:
        raise HTTPException(status_code=204, detail=str(e))

    return LastViewedGamesResponse(
        status="success",
        data=games,
        message="Last viewed games retrieved successfully"
    )
