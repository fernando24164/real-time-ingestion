from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    status: str
    message: str
    data: T | None = None
