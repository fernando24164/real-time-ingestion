from typing import Optional
from pydantic import BaseModel

class GenreBase(BaseModel):
    name: str
    description: str

class GenreCreate(GenreBase):
    pass

class GenreUpdate(GenreBase):
    name: Optional[str] = None
    description: Optional[str] = None

class GenreInDB(GenreBase):
    id: int

    class Config:
        from_attributes = True

class GenreResponse(BaseModel):
    status: str
    data: GenreInDB
    message: str