from unittest.mock import AsyncMock, Mock

import pytest
import redis
import redis.asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_redis_connection, get_pg_connection
from app.main import app


@pytest.fixture
def test_app():
    def get_test_session_factory():
        pg_mock_client = AsyncMock(spec=AsyncSession)
        pg_mock_client.add = AsyncMock(lambda: True)
        return pg_mock_client

    def get_test_redis_client():
        client_mock = AsyncMock(spec=redis.Redis)
        client_mock.lrange = AsyncMock(
            side_effect=lambda key, start, stop: [b"123"]
            if key == "last_viewed:123"
            else None
        )
        client_mock.rpush = AsyncMock(side_effect=lambda key, value: True)
        client_mock.ltrim = AsyncMock(side_effect=lambda key, start, stop: True)
        client_mock.pipeline = Mock(
            side_effect=lambda: AsyncMock(side_effect=lambda: True)
        )
        return client_mock

    redis_mock = AsyncMock(spec=redis.ConnectionPool)
    redis_mock.connection_kwargs = {"max_connections": 10}

    app.state.redis_pool = redis_mock

    app.dependency_overrides[get_redis_connection] = get_test_redis_client
    app.dependency_overrides[get_pg_connection] = get_test_session_factory
    yield app


@pytest.fixture
def client(test_app: FastAPI):
    yield TestClient(test_app)
