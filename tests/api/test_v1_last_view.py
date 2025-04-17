import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.v1.endpoints.last_games_view import last_games_view


class TestLastProductView:
    @pytest.mark.asyncio
    async def test_returns_last_viewed_games_for_valid_customer(self, mocker):
        user_id = 1
        mock_redis = mocker.AsyncMock()
        mock_redis.lrange.return_value = [b"123"]

        result = await last_games_view(
            redis_client=mock_redis, user_id=user_id
        )

        mock_redis.lrange.assert_called_once_with(f"last_viewed:{user_id}", 0, 9)
        assert result.data.last_viewed_games == ["123"]

    @pytest.mark.asyncio
    async def test_raises_404_when_no_games_exists(self, mocker):
        user_id = 456
        mock_redis = mocker.AsyncMock()
        mock_redis.lrange.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await last_games_view(redis_client=mock_redis, user_id=user_id)

        assert exc_info.value.status_code == 204
        assert "No last viewed games found" in str(exc_info.value.detail)
        mock_redis.lrange.assert_called_once_with(f"last_viewed:{user_id}", 0, 9)


class TestLastProductViewEndpoint:
    def test_get_last_viewed_product_success(self, client: TestClient):
        user_id = 123
        expected_product = ["123"]

        response = client.get(f"/api/v1/last_games_viewed?user_id={user_id}")

        assert response.status_code == 200
        assert response.json().get('data') == {"last_viewed_games": expected_product}

    def test_get_last_viewed_product_not_found(self, client: TestClient):
        user_id = 456

        response = client.get(f"/api/v1/last_games_viewed?user_id={user_id}")

        assert response.status_code == 204

    def test_get_last_viewed_product_invalid_user_id(self, client: TestClient):
        invalid_user_id = "invalid"

        response = client.get(
            f"/api/v1/last_games_viewed?user_id={invalid_user_id}"
        )

        assert response.status_code == 422
        assert "be a valid integer" in response.json()["detail"][0]["msg"]

    def test_get_last_viewed_product_missing_user_id(self, client: TestClient):
        response = client.get("/api/v1/last_games_viewed")

        assert response.status_code == 422
        assert "Field required" in response.json()["detail"][0]["msg"]
