from datetime import datetime

from pydantic import BaseModel, Field


class SessionInsights(BaseModel):
    """
    Schema for session insights stored in Redis
    """

    user_id: int
    session_id: str
    start_time: datetime
    last_activity: datetime
    page_views: int = 0
    games_viewed: list[int] = Field(default_factory=list)
    total_time_spent: int = 0
    event_counts: dict[str, int] = Field(default_factory=dict)
    referrer_pages: list[str] = Field(default_factory=list)
    duration_seconds: float | None = None

    class Config:
        from_attributes = True


class SessionInsightsResponse(BaseModel):
    """
    API response model for session insights
    """

    session_id: str
    user_id: int
    start_time: datetime
    last_activity: datetime
    duration_minutes: float = Field(..., description="Session duration in minutes")
    page_views: int
    unique_games_viewed: int
    avg_time_per_page: float | None = Field(
        None,
        description="Average time spent per page in seconds",
    )
    event_breakdown: dict[str, int] = Field(..., description="Count of each event type")
    engagement_level: str = Field(
        ...,
        description="Low, Medium, or High based on activity",
    )

    @classmethod
    def from_session_insights(
        cls,
        insights: SessionInsights,
    ) -> "SessionInsightsResponse":
        """Convert raw session insights to API response format"""
        duration_minutes = (
            insights.duration_seconds / 60 if insights.duration_seconds else 0
        )
        unique_games_viewed = len(insights.games_viewed)

        avg_time_per_page = None
        if insights.page_views > 0:
            avg_time_per_page = insights.total_time_spent / insights.page_views

        engagement_level = "Low"
        if insights.page_views >= 5 or duration_minutes >= 10:
            engagement_level = "Medium"
        if insights.page_views >= 10 or duration_minutes >= 20:
            engagement_level = "High"

        return cls(
            session_id=insights.session_id,
            user_id=insights.user_id,
            start_time=insights.start_time,
            last_activity=insights.last_activity,
            duration_minutes=duration_minutes,
            page_views=insights.page_views,
            unique_games_viewed=unique_games_viewed,
            avg_time_per_page=avg_time_per_page,
            event_breakdown=insights.event_counts,
            engagement_level=engagement_level,
        )
