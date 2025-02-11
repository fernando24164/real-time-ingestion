import datetime

import pytest

from app.schemas.ingestion import IngestionSchema


class TestIngestionSchema:
    def test_create_valid_schema_with_required_fields(self):
        timestamp = datetime.datetime.now()
        schema = IngestionSchema(customer_id=123, timestamp=timestamp, page="/home")

        assert schema.customer_id == 123
        assert schema.timestamp == timestamp
        assert schema.page == "/home"
        assert schema.product_id is None
        assert schema.genre is None
        assert schema.price is None

    def test_create_schema_without_customer_id_fails(self):
        timestamp = datetime.datetime.now()
        with pytest.raises(ValueError):
            IngestionSchema(timestamp=timestamp, page="/home")

    def test_create_schema_with_minimum_valid_values(self):
        timestamp = datetime.datetime.now()
        schema = IngestionSchema(customer_id=1, timestamp=timestamp, page="/")

        assert schema.customer_id == 1
        assert schema.timestamp == timestamp
        assert schema.page == "/"
        assert schema.product_id is None
        assert schema.genre is None
        assert schema.price is None

    def test_create_schema_without_customer_id(self):
        timestamp = datetime.datetime.now()

        with pytest.raises(ValueError) as excinfo:
            IngestionSchema(timestamp=timestamp, page="/home")

        assert "validation error" in str(excinfo.value)
