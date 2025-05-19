from fastapi import APIRouter, Path, HTTPException, status
from app.api.deps import RedisConnectionDep
from app.services.ingestion_service import get_session_insights
from app.schemas.session_insights import SessionInsights, SessionInsightsResponse

session_router = APIRouter(tags=["Session Insights"])


@session_router.get(
    "/sessions/{session_id}/insights",
    response_model=SessionInsightsResponse,
    description="Get insights for a specific user session"
)
async def get_session_analytics(
    redis_client: RedisConnectionDep,
    session_id: str = Path(..., description="Session ID to analyze"),
) -> SessionInsightsResponse:
    """
    Retrieve analytics and insights for a specific user session.
    
    This endpoint provides:
    - Session duration and activity metrics
    - Page view counts and time spent
    - Games viewed during the session
    - Event type breakdown
    - Engagement level assessment
    
    The data is collected in real-time as events are ingested.
    """
    session_data = await get_session_insights(redis_client, session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found"
        )
    
    session_insights = SessionInsights(**session_data)
    
    return SessionInsightsResponse.from_session_insights(session_insights)