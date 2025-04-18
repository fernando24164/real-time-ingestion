from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class GenrePreference(BaseModel):
    genre_id: int
    genre_name: str
    view_count: int

class UserPreferences(BaseModel):
    preferred_platform: Optional[str]
    avg_viewing_time: int
    common_filters: List[str]
    price_sensitive: bool
    preferred_genres: List[GenrePreference]

class GameRecommendation(BaseModel):
    game_id: int
    view_count: int
    last_viewed: datetime
    genres: List[str]

class PlatformStats(BaseModel):
    platform: str
    usage_count: int
    avg_time_spent: int

class CustomerInsightResponse(BaseModel):
    user_id: int
    preferences: UserPreferences
    recent_interests: List[GameRecommendation]
    platform_usage: List[PlatformStats]
    engagement_score: int  # 0-100 scale

    class Config:
        from_attributes = True
