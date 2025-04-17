from typing import List

import redis.asyncio as redis

from app.schemas.last_viewed import LastViewedGames
from app.services.exceptions import NoLastViewed


async def get_last_viewed(
    user_id: int, redis_client: redis.Redis, start: int = 0, stop: int = 9
) -> LastViewedGames:
    games: List[bytes] = await redis_client.lrange(
        f"last_viewed:{user_id}", start, stop
    )
    if not games:
        raise NoLastViewed(
            f"No last viewed games found for the user {user_id}"
        )

    games_decoded = [game.decode("utf-8") for game in games]

    return LastViewedGames(last_viewed_games=games_decoded)
