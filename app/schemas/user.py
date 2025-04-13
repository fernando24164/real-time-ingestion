from datetime import datetime

from pydantic import BaseModel

from app.schemas.response_base import ResponseBase


class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(ResponseBase[User]):
    pass
