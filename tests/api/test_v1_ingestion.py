from datetime import datetime

import pytest
from fastapi import BackgroundTasks
from pydantic import ValidationError

from app.api.v1.endpoints.ingestion import ingest_data
from app.schemas.ingestion import IngestionSchema


class TestIngestData:
    @pytest.mark.asyncio
    async def test_valid_ingestion_data_processed(self, mocker):
        mock_client = mocker.AsyncMock()
        pg_mock_client = mocker.AsyncMock()
        mocker.patch("fastapi.background.BackgroundTasks.add_task")

        test_data = IngestionSchema(
            user_id=123,
            game_id=456,
            event_type="VIEW",
            session_id="test-session",
            timestamp=datetime.now(),
            referrer_page="/test-page",
        )

        response = await ingest_data(
            data=test_data,
            background_tasks=BackgroundTasks,
            redis_client=mock_client,
            postgres_session=pg_mock_client,
        )

        assert response.status == "accepted"

    @pytest.mark.asyncio
    async def test_missing_required_fields(self, mocker):
        mock_client = mocker.AsyncMock()
        pg_mock_client = mocker.AsyncMock()
        background_tasks = BackgroundTasks()

        invalid_data = {"game_id": 456, "genre": "test", "price": 9.99}

        with pytest.raises(ValidationError):
            await ingest_data(
                data=IngestionSchema(**invalid_data),
                background_tasks=background_tasks,
                redis_client=mock_client,
                postgres_session=pg_mock_client,
            )


class TestIngestDataEndpoint:
    @pytest.mark.asyncio
    def test_ingest_data_endpoint(self, client):
        test_data = {
            "user_id": 123,
            "timestamp": datetime.now().isoformat(),
            "referrer_page": "/test-page",
            "game_id": 456,
            "event_type": "VIEW",
            "session_id": "test-session",
        }

        response = client.post("/api/v1/ingest", json=test_data)

        assert response.status_code == 202
        assert response.json().get('status') == "accepted"

    @pytest.mark.asyncio
    def test_ingest_data_endpoint_invalid_data(self, client):
        invalid_data = {"game_id": 456}

        response = client.post("/api/v1/ingest", json=invalid_data)
        assert response.status_code == 422
