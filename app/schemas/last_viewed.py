from pydantic import BaseModel

from app.schemas.response_base import ResponseBase


class LastViewedGames(BaseModel):
    last_viewed_games: list[str]


class LastViewedGamesResponse(ResponseBase[LastViewedGames]):
    pass
