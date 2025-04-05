from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.user import User
from app.services.user_service import get_user_by_id


class TestUser:
    @pytest.mark.asyncio
    async def test_user_returns_user_when_valid_customer_id(self):
        mock_user_model = MagicMock()
        mock_user_model.id = 1
        mock_user_model.username = "testuser"
        mock_user_model.email = "test@example.com"
        mock_user_model.created_at = datetime.now()
        mock_user_model.is_active = True

        expected_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            created_at=mock_user_model.created_at,
        )

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_scalars = MagicMock()

        mock_session.execute.return_value = mock_result
        mock_result.scalars.return_value = mock_scalars
        mock_scalars.first.return_value = mock_user_model

        # Act
        result = await get_user_by_id(customer_id=1, postgres_session=mock_session)

        # Assert
        mock_session.execute.assert_called_once()
        mock_result.scalars.assert_called_once()
        mock_scalars.first.assert_called_once()

        assert result.id == expected_user.id
        assert result.username == expected_user.username
        assert result.email == expected_user.email
        assert result.created_at == expected_user.created_at
