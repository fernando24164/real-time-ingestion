import datetime

import pytest

from app.schemas.ingestion import IngestionSchema


class TestIngestionSchema:
    def test_create_valid_schema_with_required_fields(self):
        timestamp = datetime.datetime.now()
        schema = IngestionSchema(
            user_id=123,
            timestamp=timestamp,
            referrer_page="/home",
            event_type="VIEW",
            session_id="session_1",
        )

        assert schema.user_id == 123
        assert schema.timestamp == timestamp
        assert schema.referrer_page == "/home"
        assert schema.game_id is None
        assert schema.event_type == "VIEW"
        assert schema.session_id == "session_1"

    def test_create_schema_without_user_id_fails(self):
        timestamp = datetime.datetime.now()
        with pytest.raises(ValueError):
            IngestionSchema(timestamp=timestamp, referrer_page="/home")

    def test_create_schema_with_minimum_valid_values(self):
        timestamp = datetime.datetime.now()
        schema = IngestionSchema(
            user_id=123,
            timestamp=timestamp,
            referrer_page="/home",
            event_type="VIEW",
            session_id="session_1",
        )
        assert schema.user_id == 123
        assert schema.timestamp == timestamp
        assert schema.referrer_page == "/home"
        assert schema.game_id is None
        assert schema.event_type == "VIEW"
        assert schema.session_id == "session_1"

    def test_create_schema_without_user_id(self):
        timestamp = datetime.datetime.now()

        with pytest.raises(ValueError) as excinfo:
            IngestionSchema(timestamp=timestamp, referrer_page="/home")

        assert "validation error" in str(excinfo.value)
