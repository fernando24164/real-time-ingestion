from typing import List, Tuple, Dict
from sqlalchemy import select, desc, func, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.game_store import WebEvents, Game, Genre, game_genre
from app.schemas.customer_insights import (
    GameRecommendation,
    PlatformStats,
    UserPreferences,
    GenrePreference,
)

# Constants
ENGAGEMENT_WINDOW_DAYS = 7
ENGAGEMENT_SCORE_MULTIPLIER = 10
ENGAGEMENT_SCORE_MAX = 100


async def get_user_platform_preferences(
    db: AsyncSession, user_id: int
) -> Tuple[str, int]:
    """Get user's preferred platform and usage count"""
    stmt = (
        select(WebEvents.platform, func.count(WebEvents.id).label("count"))
        .filter(WebEvents.user_id == user_id)
        .group_by(WebEvents.platform)
        .order_by(desc("count"))
    )
    result = await db.execute(stmt)
    platform_stats = result.first()
    return platform_stats[0], platform_stats[1] if platform_stats else ("", 0)


async def get_user_filters(db: AsyncSession, user_id: int) -> List[str]:
    """Get user's commonly used filters"""
    stmt = (
        select(WebEvents.filters_applied)
        .filter(WebEvents.user_id == user_id, WebEvents.filters_applied.isnot(None))
        .order_by(desc(WebEvents.timestamp))
        .limit(10)
    )
    result = await db.execute(stmt)
    filters = {f for (f,) in result.all() if f}  # Using a set directly
    return list(filters)


async def get_average_viewing_time(db: AsyncSession, user_id: int) -> int:
    """Calculate average time spent viewing games"""
    stmt = select(func.avg(WebEvents.time_spent)).filter(
        WebEvents.user_id == user_id, WebEvents.event_type == "VIEW"
    )
    result = await db.execute(stmt)
    return int(result.scalar() or 0)


async def get_user_preferences(db: AsyncSession, user_id: int) -> UserPreferences:
    """Analyze user preferences based on their web events"""
    preferred_platform, platform_count = await get_user_platform_preferences(
        db, user_id
    )
    filters = await get_user_filters(db, user_id)
    avg_time = await get_average_viewing_time(db, user_id)
    preferred_genres = await get_genre_preferences(db, user_id)

    return UserPreferences(
        preferred_platform=preferred_platform,
        avg_viewing_time=avg_time,
        common_filters=filters,
        price_sensitive=any("price_under" in (f or "") for f in filters),
        preferred_genres=preferred_genres,
    )


async def get_game_genres(
    db: AsyncSession, game_ids: List[int]
) -> Dict[int, List[str]]:
    """Get genres for multiple games"""
    stmt = select(Game).options(joinedload(Game.genres)).filter(Game.id.in_(game_ids))
    result = await db.execute(stmt)
    games = result.unique().scalars().all()

    return {game.id: [genre.name for genre in game.genres] for game in games}


async def get_genre_preferences(
    db: AsyncSession, user_id: int
) -> List[GenrePreference]:
    """Get user's preferred genres based on viewing history"""
    stmt = (
        select(Genre.id, Genre.name, func.count(WebEvents.id).label("view_count"))
        .join(game_genre, Genre.id == game_genre.c.genre_id)
        .join(Game, Game.id == game_genre.c.game_id)
        .join(
            WebEvents,
            and_(
                WebEvents.game_id == Game.id,
                WebEvents.user_id == user_id,
                WebEvents.event_type == "VIEW",
            ),
        )
        .group_by(Genre.id, Genre.name)
        .order_by(desc("view_count"))
        .limit(5)
    )

    result = await db.execute(stmt)
    return [
        GenrePreference(genre_id=genre_id, genre_name=name, view_count=count)
        for genre_id, name, count in result.all()
    ]


async def get_recent_interests(
    db: AsyncSession, user_id: int
) -> List[GameRecommendation]:
    """Get user's recently viewed games with their genres"""
    stmt = (
        select(
            WebEvents.game_id,
            func.count(WebEvents.id).label("view_count"),
            func.max(WebEvents.timestamp).label("last_viewed"),
        )
        .filter(
            WebEvents.user_id == user_id,
            WebEvents.game_id.isnot(None),
            WebEvents.event_type == "VIEW",
        )
        .group_by(WebEvents.game_id)
        .order_by(desc("last_viewed"))
        .limit(5)
    )
    result = await db.execute(stmt)
    games_data = result.all()

    # Get genres for all games in one query
    game_ids = [game_id for game_id, _, _ in games_data]
    game_genres = await get_game_genres(db, game_ids)

    return [
        GameRecommendation(
            game_id=game_id,
            view_count=view_count,
            last_viewed=last_viewed,
            genres=game_genres.get(game_id, []),
        )
        for game_id, view_count, last_viewed in games_data
    ]


async def get_platform_usage(db: AsyncSession, user_id: int) -> List[PlatformStats]:
    """Get platform usage statistics"""
    stmt = (
        select(
            WebEvents.platform,
            func.count(WebEvents.id).label("usage_count"),
            func.avg(WebEvents.time_spent).label("avg_time"),
        )
        .filter(WebEvents.user_id == user_id)
        .group_by(WebEvents.platform)
    )
    result = await db.execute(stmt)

    return [
        PlatformStats(
            platform=platform, usage_count=int(count), avg_time_spent=int(avg_time or 0)
        )
        for platform, count, avg_time in result.all()
    ]


async def calculate_engagement_score(db: AsyncSession, user_id: int) -> int:
    """Calculate user engagement score"""
    stmt = select(func.count(WebEvents.id)).filter(
        WebEvents.user_id == user_id,
        WebEvents.timestamp
        >= func.now() - text(f"interval '{ENGAGEMENT_WINDOW_DAYS} days'"),
    )
    result = await db.execute(stmt)
    score = result.scalar() or 0
    return min(score * ENGAGEMENT_SCORE_MULTIPLIER, ENGAGEMENT_SCORE_MAX)  # Scale 0-100
