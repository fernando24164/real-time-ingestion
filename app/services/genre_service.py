from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game_store import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from app.services.exceptions import DuplicateEntry, NoGenre


async def create_genre(db: AsyncSession, genre: GenreCreate) -> Genre:
    db_genre = Genre(**genre.model_dump())
    try:
        db.add(db_genre)
        await db.commit()
        await db.refresh(db_genre)
        return db_genre
    except IntegrityError as e:
        await db.rollback()
        msg = f"Genre with name {genre.name} already exists"
        raise DuplicateEntry(msg) from e


async def get_genre(db: AsyncSession, genre_id: int) -> Genre:
    result = await db.execute(select(Genre).filter(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        msg = f"Genre with id {genre_id} not found"
        raise NoGenre(msg)
    return genre


async def get_genres(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Genre]:
    result = await db.execute(select(Genre).offset(skip).limit(limit))
    genres = result.scalars().all()
    if not genres:
        msg = "No genres found"
        raise NoGenre(msg)
    return list(genres)


async def update_genre(
    db: AsyncSession,
    genre_id: int,
    genre: GenreUpdate,
) -> Genre:
    db_genre = await get_genre(db, genre_id)

    update_data = genre.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_genre, field, value)

    try:
        await db.commit()
        await db.refresh(db_genre)
        return db_genre
    except IntegrityError as e:
        await db.rollback()
        msg = f"Genre with name {genre.name} already exists"
        raise DuplicateEntry(msg) from e


async def delete_genre(db: AsyncSession, genre_id: int) -> None:
    db_genre = await get_genre(db, genre_id)
    await db.delete(db_genre)
    await db.commit()
