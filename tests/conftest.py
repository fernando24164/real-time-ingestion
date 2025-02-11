from unittest.mock import AsyncMock, Mock

import pytest
import redis
from fastapi import FastAPI
from fastapi.testclient import TestClient
from opensearchpy._async.client import AsyncOpenSearch
import redis.asyncio

from app.api.deps import get_async_opensearch_client, get_redis_connection
from app.main import app


@pytest.fixture
def test_app():
    def get_test_opensearch_client():
        client_mock = AsyncMock(spec=AsyncOpenSearch)
        client_mock.index = AsyncMock(side_effect=lambda index, body, refresh: True)
        return client_mock

    def get_test_redis_client():
        client_mock = AsyncMock(spec=redis.Redis)
        client_mock.get = AsyncMock(side_effect=lambda key: b"product_123" if key == "last_viewed:123" else None)
        client_mock.rpush = AsyncMock(side_effect=lambda key, value: True)
        client_mock.ltrim = AsyncMock(side_effect=lambda key, start, stop: True)
        return client_mock

    redis_mock = AsyncMock(spec=redis.ConnectionPool)
    redis_mock.connection_kwargs = {"max_connections": 10}

    app.state.redis_pool = redis_mock

    app.dependency_overrides[get_async_opensearch_client] = get_test_opensearch_client
    app.dependency_overrides[get_redis_connection] = get_test_redis_client
    yield app


@pytest.fixture
def client(test_app: FastAPI):
    yield TestClient(test_app)
