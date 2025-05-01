from pydantic import BaseModel


class GameBase(BaseModel):
    title: str
    description: str
    price: float
    release_date: str
    publisher_id: int
    platform: str
    stock: int
    is_digital: bool
    is_active: bool
    region: str
    condition_rating: int
    has_original_box: bool
    has_manual: bool
    is_rare: bool
    collector_value: float
    serial_number: str
    special_edition: bool
    genres: list[str]
    reviews: list[str]

    class Config:
        from_attributes = True


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


class GameInDB(GameBase):
    id: int

    class Config:
        from_attributes = True


class GameResponse(BaseModel):
    status: str
    data: GameInDB
    message: str
