from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str
    description: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    name: str | None = None
    description: str | None = None


class GenreInDB(GenreBase):
    id: int

    class Config:
        from_attributes = True


class GenreResponse(BaseModel):
    status: str
    data: GenreInDB
    message: str
