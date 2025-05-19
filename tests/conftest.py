import json
from datetime import datetime, timedelta
from typing import Any, Generator, Optional
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
import redis.asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_pg_connection, get_redis_connection
from app.main import app


@pytest.fixture
def mock_postgres_session() -> AsyncMock:
    pg_mock_client = AsyncMock(spec=AsyncSession)
    pg_mock_client.add = AsyncMock(return_value=True)
    pg_mock_client.commit = AsyncMock(return_value=True)
    pg_mock_client.close = AsyncMock(return_value=True)
    return pg_mock_client


@pytest.fixture
def mock_redis_client() -> AsyncMock:
    client_mock = AsyncMock(spec=redis.asyncio.Redis)

    async def mock_lrange(key: str, start: int, stop: int) -> list:
        if key == "last_viewed:123":
            return [b"123"]
        return []

    async def mock_hget(key: str, field: str) -> Optional[bytes]:
        if "session:insights:" in key:
            if field == "event_counts":
                return json.dumps({"VIEW": 5, "CLICK": 2}).encode('utf-8')
            elif field == "games_viewed":
                return json.dumps([102, 103, 104]).encode('utf-8')
            elif field == "referrer_pages":
                return json.dumps(["/games", "/home"]).encode('utf-8')
        return None

    async def mock_hgetall(key: str) -> dict:
        if "session:insights:" in key:
            session_data = {
                "user_id": "123",
                "session_id": key.split(":")[-1],
                "start_time": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "last_activity": datetime.now().isoformat(),
                "page_views": "15",
                "games_viewed": json.dumps([101, 102, 103]),
                "total_time_spent": "450",
                "event_counts": json.dumps({"VIEW": 10, "CLICK": 5}),
                "referrer_pages": json.dumps(["/home", "/games"])
            }
            return {k.encode('utf-8'): v.encode('utf-8') for k, v in session_data.items()}
        return {}

    # Set up mock methods
    client_mock.lrange = AsyncMock(side_effect=mock_lrange)
    client_mock.hget = AsyncMock(side_effect=mock_hget)
    client_mock.hgetall = AsyncMock(side_effect=mock_hgetall)
    client_mock.exists = AsyncMock(return_value=True)
    client_mock.rpush = AsyncMock(return_value=True)
    client_mock.ltrim = AsyncMock(return_value=True)

    pipeline_mock = MagicMock()
    pipeline_mock.execute = AsyncMock(return_value=[True])
    client_mock.pipeline = Mock(return_value=pipeline_mock)

    return client_mock


@pytest.fixture
def mock_redis_pool() -> AsyncMock:
    redis_mock = AsyncMock(spec=redis.asyncio.ConnectionPool)
    redis_mock.connection_kwargs = {
        "max_connections": 10,
        "host": "localhost",
        "port": 6379,
        "db": 0,
    }
    return redis_mock


@pytest.fixture
def test_app(
    mock_redis_pool: AsyncMock,
    mock_redis_client: AsyncMock,
    mock_postgres_session: AsyncMock,
) -> Generator[FastAPI, Any, Any]:
    app.state.redis_pool = mock_redis_pool

    app.dependency_overrides[get_redis_connection] = lambda: mock_redis_client
    app.dependency_overrides[get_pg_connection] = lambda: mock_postgres_session

    try:
        yield app
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)
