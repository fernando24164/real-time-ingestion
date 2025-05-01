from typing import Optional
from pydantic import BaseModel, HttpUrl

class PublisherBase(BaseModel):
    name: str
    website: Optional[HttpUrl] = None
    founded_year: Optional[int] = None

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(PublisherBase):
    name: Optional[str] = None

class PublisherInDB(PublisherBase):
    id: int

    class Config:
        from_attributes = True

class PublisherResponse(BaseModel):
    status: str
    data: PublisherInDB
    message: str