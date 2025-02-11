from typing import Optional

from pydantic import BaseModel, NaiveDatetime


class IngestionSchema(BaseModel):
    """
    A Pydantic model for data ingestion schema, used for customer activity tracking.

    Attributes:
        customer_id (int): Required. Identifier for the customer.
        product_id (Optional[int]): Optional. Identifier for the product.
        genre (Optional[str]): Optional. Category or genre of the product.
        price (Optional[float]): Optional. Price of the product.
        timestamp (datetime): Required. Time of the event.
        page (str): Required. Webpage location of the event.
    """

    customer_id: int
    product_id: Optional[int] = None
    genre: Optional[str] = None
    price: Optional[float] = None
    timestamp: NaiveDatetime
    page: str
