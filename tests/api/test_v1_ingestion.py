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
        mocker.patch("fastapi.background.BackgroundTasks.add_task")

        test_data = IngestionSchema(
            customer_id=123,
            timestamp=datetime.now(),
            page="/test-page",
            product_id=456,
            genre="test",
            price=9.99,
        )

        response = await ingest_data(
            data=test_data,
            background_tasks=BackgroundTasks,
            opensearch_client=mock_client,
            redis_client=mock_client,
        )

        assert response == {"message": "Data ingested successfully"}

    @pytest.mark.asyncio
    async def test_missing_required_fields(self, mocker):
        mock_client = mocker.AsyncMock()

        invalid_data = {"product_id": 456, "genre": "test", "price": 9.99}

        with pytest.raises(ValidationError):
            await ingest_data(
                data=IngestionSchema(**invalid_data), opensearch_client=mock_client
            )


class TestIngestDataEndpoint:
    @pytest.mark.asyncio
    def test_ingest_data_endpoint(self, client):
        test_data = {
            "customer_id": 123,
            "timestamp": datetime.now().isoformat(),
            "page": "/test-page",
            "product_id": 456,
            "genre": "test",
            "price": 9.99,
        }

        response = client.post("/api/v1/ingest", json=test_data)

        assert response.status_code == 200
        assert response.json() == {"message": "Data ingested successfully"}

    @pytest.mark.asyncio
    def test_ingest_data_endpoint_invalid_data(self, client):
        invalid_data = {"product_id": 456, "genre": "test", "price": 9.99}

        response = client.post("/api/v1/ingest", json=invalid_data)
        assert response.status_code == 422
