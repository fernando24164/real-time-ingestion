from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GenrePreference(BaseModel):
    genre_id: int
    genre_name: str
    view_count: int


class UserPreferences(BaseModel):
    preferred_platform: str | None
    avg_viewing_time: int
    common_filters: list[str]
    price_sensitive: bool
    preferred_genres: list[GenrePreference]


class GameRecommendation(BaseModel):
    game_id: int
    view_count: int
    last_viewed: datetime
    genres: list[str]


class PlatformStats(BaseModel):
    platform: str
    usage_count: int
    avg_time_spent: int


class CustomerInsightResponse(BaseModel):
    user_id: int
    preferences: UserPreferences
    recent_interests: list[GameRecommendation]
    platform_usage: list[PlatformStats]
    engagement_score: int  # 0-100 scale

    model_config = ConfigDict(from_attributes=True)
