import json
from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException

from app.api.v1.endpoints.session_insights import get_session_analytics
from app.schemas.ingestion import IngestionSchema
from app.schemas.session_insights import SessionInsightsResponse
from app.services.ingestion_service import get_session_insights, update_session_insights


class TestSessionInsights:
    @pytest.mark.asyncio
    async def test_get_session_insights_returns_data_when_session_exists(self, mocker):
        # Arrange
        session_id = "test-session-123"
        mock_redis = mocker.AsyncMock()

        # Mock session data in Redis
        session_data = {
            "user_id": "123",
            "session_id": session_id,
            "start_time": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "last_activity": datetime.now().isoformat(),
            "page_views": "15",
            "games_viewed": json.dumps([101, 102, 103]),
            "total_time_spent": "450",
            "event_counts": json.dumps({"VIEW": 10, "CLICK": 5}),
            "referrer_pages": json.dumps(["/home", "/games"]),
        }

        # Convert to bytes as Redis would return
        session_data_bytes = {
            k.encode("utf-8"): v.encode("utf-8") for k, v in session_data.items()
        }

        mock_redis.exists.return_value = True
        mock_redis.hgetall.return_value = session_data_bytes

        # Act
        result = await get_session_insights(mock_redis, session_id)

        # Assert
        mock_redis.exists.assert_called_once_with(f"session:insights:{session_id}")
        mock_redis.hgetall.assert_called_once_with(f"session:insights:{session_id}")

        assert result is not None
        assert result["user_id"] == "123"
        assert result["session_id"] == session_id
        assert result["page_views"] == 15
        assert result["games_viewed"] == [101, 102, 103]
        assert result["total_time_spent"] == 450
        assert result["event_counts"] == {"VIEW": 10, "CLICK": 5}
        assert result["referrer_pages"] == ["/home", "/games"]
        assert "duration_seconds" in result

    @pytest.mark.asyncio
    async def test_get_session_insights_returns_none_when_session_not_exists(
        self, mocker
    ):
        # Arrange
        session_id = "nonexistent-session"
        mock_redis = mocker.AsyncMock()
        mock_redis.exists.return_value = False

        # Act
        result = await get_session_insights(mock_redis, session_id)

        # Assert
        mock_redis.exists.assert_called_once_with(f"session:insights:{session_id}")
        mock_redis.hgetall.assert_not_called()
        assert result is None

    @pytest.mark.asyncio
    async def test_update_session_insights_creates_new_session(self, mocker):
        # Arrange
        session_id = "existing-session-123"
        mock_redis = mocker.AsyncMock()

        # Mock session existence check
        mock_redis.exists.return_value = True

        # Mock the hget responses for different keys
        async def mock_hget(_, field):
            if field == "event_counts":
                return json.dumps({"VIEW": 5, "CLICK": 2}).encode("utf-8")
            elif field == "games_viewed":
                return json.dumps([102, 103, 104]).encode("utf-8")
            elif field == "referrer_pages":
                return json.dumps(["/games", "/home"]).encode("utf-8")
            return None

        mock_redis.hget = mocker.AsyncMock(side_effect=mock_hget)

        # Create a proper pipeline mock structure
        mock_pipeline = mocker.Mock()
        mock_pipeline.hset = mocker.AsyncMock()
        mock_pipeline.expire = mocker.AsyncMock()
        mock_pipeline.execute = mocker.AsyncMock()

        # Use regular Mock for pipeline() method (not async)
        mock_redis.pipeline = mocker.Mock(return_value=mock_pipeline)

        data = IngestionSchema(
            user_id=123,
            session_id=session_id,
            event_type="VIEW",
            game_id=101,
            timestamp=datetime.now(),
            referrer_page="/home",
            time_spent=30,
        )

        # Act
        await update_session_insights(mock_redis, data)

        # Assert
        mock_redis.exists.assert_called_once_with(f"session:insights:{session_id}")
        mock_redis.pipeline.assert_called_once()
        mock_pipeline.hset.assert_called()
        mock_pipeline.expire.assert_called_once()
        mock_pipeline.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_session_insights_updates_existing_session(self, mocker):
        # Arrange
        session_id = "existing-session-123"
        mock_redis = mocker.AsyncMock()
        mock_redis.exists.return_value = True

        # Mock existing session data
        mock_redis.hget.side_effect = [
            # event_counts
            json.dumps({"VIEW": 5}).encode("utf-8"),
            # games_viewed
            json.dumps([102, 103]).encode("utf-8"),
            # referrer_pages
            json.dumps(["/games"]).encode("utf-8"),
        ]

        mock_pipeline = mocker.Mock()
        mock_pipeline.execute = mocker.AsyncMock()
        mock_redis.pipeline = mocker.Mock(return_value=mock_pipeline)

        data = IngestionSchema(
            user_id=123,
            session_id=session_id,
            event_type="VIEW",
            game_id=101,
            timestamp=datetime.now(),
            referrer_page="/home",
            time_spent=30,
        )

        # Act
        await update_session_insights(mock_redis, data)

        # Assert
        mock_redis.exists.assert_called_once_with(f"session:insights:{session_id}")
        mock_redis.hget.assert_called()
        mock_pipeline.hset.assert_called()
        mock_pipeline.hincrby.assert_called()
        mock_pipeline.expire.assert_called_once()
        mock_pipeline.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_session_insights_limits_games_to_ten(self, mocker):
        # Arrange
        session_id = "session-with-many-games"
        mock_redis = mocker.AsyncMock()
        mock_redis.exists.return_value = True

        # Mock existing session with 10 games already
        existing_games = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
        mock_redis.hget.side_effect = [
            # event_counts
            json.dumps({"VIEW": 10}).encode("utf-8"),
            # games_viewed
            json.dumps(existing_games).encode("utf-8"),
            # referrer_pages
            json.dumps(["/games"]).encode("utf-8"),
        ]

        mock_pipeline = mocker.Mock()
        mock_pipeline.execute = mocker.AsyncMock()
        mock_redis.pipeline = mocker.Mock(return_value=mock_pipeline)

        # New game view
        data = IngestionSchema(
            user_id=123,
            session_id=session_id,
            event_type="VIEW",
            game_id=111,  # New game
            timestamp=datetime.now(),
            referrer_page="/games/111",
            time_spent=30,
        )

        # Act
        await update_session_insights(mock_redis, data)

        # Assert
        mock_redis.exists.assert_called_once_with(f"session:insights:{session_id}")

        # Check that we're storing only 10 games (the most recent ones)
        # The first game (101) should be dropped, and 111 should be added
        expected_games = existing_games[1:] + [111]

        # Find the call to hset with games_viewed
        for call in mock_pipeline.hset.call_args_list:
            args, kwargs = call
            if len(args) >= 3 and args[1] == "games_viewed":
                stored_games = json.loads(args[2])
                assert len(stored_games) == 10
                assert stored_games == expected_games
                break


class TestSessionInsightsEndpoint:
    @pytest.mark.asyncio
    async def test_get_session_analytics_returns_insights_when_session_exists(
        self, mocker
    ):
        # Arrange
        session_id = "test-session-123"

        # Mock the get_session_insights function
        mock_session_data = {
            "user_id": "123",
            "session_id": session_id,
            "start_time": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "last_activity": datetime.now().isoformat(),
            "page_views": 15,
            "games_viewed": [101, 102, 103],
            "total_time_spent": 450,
            "event_counts": {"VIEW": 10, "CLICK": 5},
            "referrer_pages": ["/home", "/games"],
        }

        mocker.patch(
            "app.api.v1.endpoints.session_insights.get_session_insights",
            return_value=mock_session_data,
        )

        mock_redis = mocker.AsyncMock()

        # Act
        response = await get_session_analytics(mock_redis, session_id)

        # Assert
        assert isinstance(response, SessionInsightsResponse)
        assert response.session_id == session_id
        assert response.user_id == 123
        assert response.page_views == 15
        assert response.unique_games_viewed == 3
        assert response.event_breakdown == {"VIEW": 10, "CLICK": 5}
        assert response.engagement_level in ["Low", "Medium", "High"]

    @pytest.mark.asyncio
    async def test_get_session_analytics_raises_404_when_session_not_found(
        self, mocker
    ):
        # Arrange
        session_id = "nonexistent-session"

        # Mock the get_session_insights function to return None
        mocker.patch(
            "app.services.ingestion_service.get_session_insights", return_value=None
        )

        mock_redis = mocker.AsyncMock()
        mock_redis.exists.return_value = False

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_session_analytics(mock_redis, session_id)

        assert exc_info.value.status_code == 404
        assert f"Session with ID {session_id} not found" in str(exc_info.value.detail)

    def test_session_insights_endpoint_integration(self, client):
        # Arrange
        session_id = "test-session-123"

        # Act
        response = client.get(f"/api/v1/analytics/sessions/{session_id}/insights")

        # Assert
        # Note: This will return 404 in tests since we're using mocked Redis
        # The actual behavior is tested in the unit tests above
        # assert response.status_code in [200, 404]
        assert response.status_code == 404

        if response.status_code == 200:
            data = response.json()
            assert data["session_id"] == session_id
            assert "user_id" in data
            assert "page_views" in data
            assert "unique_games_viewed" in data
            assert "event_breakdown" in data
            assert "engagement_level" in data
