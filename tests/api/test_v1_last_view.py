import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.v1.endpoints.last_product_view import last_product_view


class TestLastProductView:
    @pytest.mark.asyncio
    async def test_returns_last_viewed_product_for_valid_customer(self, mocker):
        customer_id = 123
        mock_redis = mocker.AsyncMock()
        mock_redis.lrange.return_value = [b"123"]

        result = await last_product_view(
            redis_client=mock_redis, customer_id=customer_id
        )

        mock_redis.lrange.assert_called_once_with(f"last_viewed:{customer_id}", 0, 9)
        assert result == {"last_viewed_product": ["123"]}

    @pytest.mark.asyncio
    async def test_raises_404_when_no_product_exists(self, mocker):
        customer_id = 456
        mock_redis = mocker.AsyncMock()
        mock_redis.lrange.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await last_product_view(redis_client=mock_redis, customer_id=customer_id)

        assert exc_info.value.status_code == 204
        assert "No last viewed products found" in str(exc_info.value.detail)
        mock_redis.lrange.assert_called_once_with(f"last_viewed:{customer_id}", 0, 9)


class TestLastProductViewEndpoint:
    def test_get_last_viewed_product_success(self, client: TestClient):
        customer_id = 123
        expected_product = ["123"]

        response = client.get(f"/api/v1/last_product_viewed?customer_id={customer_id}")

        assert response.status_code == 200
        assert response.json() == {"last_viewed_product": expected_product}

    def test_get_last_viewed_product_not_found(self, client: TestClient):
        customer_id = 456

        response = client.get(f"/api/v1/last_product_viewed?customer_id={customer_id}")

        assert response.status_code == 204

    def test_get_last_viewed_product_invalid_customer_id(self, client: TestClient):
        invalid_customer_id = "invalid"

        response = client.get(
            f"/api/v1/last_product_viewed?customer_id={invalid_customer_id}"
        )

        assert response.status_code == 422
        assert "be a valid integer" in response.json()["detail"][0]["msg"]

    def test_get_last_viewed_product_missing_customer_id(self, client: TestClient):
        response = client.get("/api/v1/last_product_viewed")

        assert response.status_code == 422
        assert "Field required" in response.json()["detail"][0]["msg"]
