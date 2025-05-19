import json
from datetime import datetime
from math import ceil
from typing import Optional

import redis.asyncio as redis
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game_store import WebEvents
from app.schemas.ingestion import IngestionSchema


async def ingest_data_service(
    data: IngestionSchema, redis_client: redis.Redis, postgres_session: AsyncSession
) -> None:
    try:
        # Store last viewed games in Redis list
        if data.game_id:
            # Update session insights in Redis
            await update_session_insights(redis_client, data)

        # Store event in PostgreSQL
        web_event = WebEvents(**data.model_dump())
        postgres_session.add(web_event)
        await postgres_session.commit()
    except Exception as e:
        logger.exception(f"Error ingesting data: {e}")
        raise


async def update_session_insights(
    redis_client: redis.Redis, data: IngestionSchema
) -> None:
    """
    Update session insights in Redis based on web events.
    This creates/updates a Redis hash with session activity metrics.
    Limits stored games viewed to the 10 most recent.
    """
    session_key = f"session:insights:{data.session_id}"

    # Check if session exists in Redis
    session_exists = await redis_client.exists(session_key)

    # Get current timestamp for calculations
    current_time = datetime.now()

    # Start a Redis pipeline for atomic operations
    pipeline = redis_client.pipeline()

    if not session_exists:
        # Initialize new session insights
        session_data = {
            "user_id": data.user_id,
            "session_id": data.session_id,
            "start_time": current_time.isoformat(),
            "last_activity": current_time.isoformat(),
            "page_views": 0,
            "games_viewed": json.dumps([]),
            "total_time_spent": 0,
            "event_counts": json.dumps({}),
            "referrer_pages": json.dumps([]),
        }
        pipeline.hset(session_key, mapping=session_data)
    else:
        # Update last activity time
        pipeline.hset(session_key, "last_activity", current_time.isoformat())

    # Update event counts
    event_counts_json = await redis_client.hget(session_key, "event_counts")
    if event_counts_json:
        event_counts = json.loads(event_counts_json.decode("utf-8"))
    else:
        event_counts = {}

    event_counts[data.event_type] = event_counts.get(data.event_type, 0) + 1
    pipeline.hset(session_key, "event_counts", json.dumps(event_counts))

    # Update page views if this is a VIEW event
    if data.event_type == "VIEW":
        pipeline.hincrby(session_key, "page_views", 1)

    # Update time spent if available
    if data.time_spent:
        pipeline.hincrby(session_key, "total_time_spent", data.time_spent)

    # Update games viewed if this is a game view
    if data.event_type == "VIEW" and data.game_id:
        games_viewed_json = await redis_client.hget(session_key, "games_viewed")
        if games_viewed_json:
            games_viewed = json.loads(games_viewed_json.decode("utf-8"))
        else:
            games_viewed = []

        if data.game_id not in games_viewed:
            # Add the new game_id to the list
            games_viewed.append(data.game_id)
            # Limit to 10 most recent games (keep the last 10)
            if len(games_viewed) > 10:
                games_viewed = games_viewed[-10:]
            pipeline.hset(session_key, "games_viewed", json.dumps(games_viewed))

    # Update referrer pages
    if data.referrer_page:
        referrer_pages_json = await redis_client.hget(session_key, "referrer_pages")
        if referrer_pages_json:
            referrer_pages = json.loads(referrer_pages_json.decode("utf-8"))
        else:
            referrer_pages = []

        if data.referrer_page not in referrer_pages:
            referrer_pages.append(data.referrer_page)
            pipeline.hset(session_key, "referrer_pages", json.dumps(referrer_pages))

    # Set expiration time (24 hours)
    pipeline.expire(session_key, 60 * 60 * 24)

    # Execute all commands atomically
    await pipeline.execute()


async def get_session_insights(redis_client: redis.Redis, session_id: str) -> Optional[dict]:
    """
    Retrieve session insights from Redis.
    Returns a dictionary with session metrics or None if not found.
    """
    session_key = f"session:insights:{session_id}"

    # Check if session exists
    if not await redis_client.exists(session_key):
        return None

    # Get all session data
    session_data = await redis_client.hgetall(session_key)

    # Convert bytes to strings
    session_data = {
        k.decode("utf-8"): v.decode("utf-8") for k, v in session_data.items()
    }

    # Parse JSON fields
    for field in ["event_counts", "games_viewed", "referrer_pages"]:
        if field in session_data:
            session_data[field] = json.loads(session_data[field])

    # Convert numeric fields
    for field in ["page_views", "total_time_spent"]:
        if field in session_data:
            session_data[field] = int(session_data[field])

    # Calculate session duration
    if "start_time" in session_data and "last_activity" in session_data:
        start_time = datetime.fromisoformat(session_data["start_time"])
        last_activity = datetime.fromisoformat(session_data["last_activity"])
        session_data["duration_seconds"] = ceil((last_activity - start_time).total_seconds())

    return session_data
