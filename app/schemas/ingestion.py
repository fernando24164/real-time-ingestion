from typing import Any

from pydantic import BaseModel, Field, NaiveDatetime


class IngestionSchema(BaseModel):
    """
    A Pydantic model for data ingestion schema, used for customer activity tracking.

    Attributes:
        user_id (int): Required. Identifier for the user.
        game_id (Optional[int]): Optional. Identifier for the game.
        event_type (str): Required. Type of event (e.g., "VIEW", "ADD_TO_CART",
        "REMOVE_FROM_CART", "WISHLIST", "PURCHASE", "REVIEW")
        session_id (str): Required. Unique identifier for the user's session.
        time_spent (Optional[int]): Optional. Time spent on the game page in seconds.
        timestamp (datetime): Required. Time of the event.
        referrer_page (str): Required. Webpage location where the event originated.
    """

    user_id: int
    game_id: int | None = None
    event_type: str
    session_id: str
    time_spent: int | None = None
    timestamp: NaiveDatetime
    referrer_page: str


class IngestionResponse(BaseModel):
    """
    Response model for data ingestion endpoints.

    Attributes:
        status (str): Status of the ingestion request (e.g., "accepted", "failed")
        message (str): Human-readable description of the result
        request_id (Any): Identifier that can be used to track this specific request
    """

    status: str = Field(..., description="Status of the ingestion request")
    message: str = Field(..., description="Human-readable description of the result")
    request_id: Any = Field(..., description="Identifier for tracking this request")
