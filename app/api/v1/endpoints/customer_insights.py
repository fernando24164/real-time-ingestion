from fastapi import APIRouter, Query

from app.api.deps import DBSessionDep
from app.schemas.customer_insights import CustomerInsightResponse
from app.services.customer_insights_service import (
    get_user_preferences,
    get_recent_interests,
    get_platform_usage,
    calculate_engagement_score
)

insights_router = APIRouter(tags=["Customer Insights"])


@insights_router.get(
    "/customer/insights",
    response_model=CustomerInsightResponse,
    description="Generate personalized customer insights including genre preferences"
)
async def get_customer_insights(
    db: DBSessionDep,
    user_id: int = Query(..., description="User ID to analyze"),
) -> CustomerInsightResponse:
    """
    Generate personalized insights for a customer based on their web events.
    
    This endpoint analyzes:
    - User preferences (platform, filters, viewing time)
    - Genre preferences based on viewing history
    - Recent interests with associated genres
    - Platform usage statistics
    - Overall engagement score
    
    Returns a comprehensive analysis of the user's behavior and preferences.
    """
    preferences = await get_user_preferences(db, user_id)
    recent_interests = await get_recent_interests(db, user_id)
    platform_usage = await get_platform_usage(db, user_id)
    engagement_score = await calculate_engagement_score(db, user_id)

    return CustomerInsightResponse(
        user_id=user_id,
        preferences=preferences,
        recent_interests=recent_interests,
        platform_usage=platform_usage,
        engagement_score=engagement_score
    )
