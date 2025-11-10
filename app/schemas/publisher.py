from pydantic import BaseModel, ConfigDict, HttpUrl


class PublisherBase(BaseModel):
    name: str
    website: HttpUrl | None = None
    founded_year: int | None = None


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(PublisherBase):
    name: str | None = None


class PublisherInDB(PublisherBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PublisherResponse(BaseModel):
    status: str
    data: PublisherInDB
    message: str
