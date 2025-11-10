from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.response_base import ResponseBase


class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool
    created_at: datetime
    orders: list[int]
    reviews: list[int]

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True


class UserUpdate(BaseModel):
    username: str
    email: str
    is_active: bool


class UserResponse(ResponseBase[User]):
    pass
