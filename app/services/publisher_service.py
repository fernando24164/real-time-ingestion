from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game_store import Publisher
from app.schemas.publisher import PublisherCreate, PublisherUpdate
from app.services.exceptions import DuplicateEntry, NoPublisher


async def create_publisher(db: AsyncSession, publisher: PublisherCreate) -> Publisher:
    db_publisher = Publisher(**publisher.model_dump())
    try:
        db.add(db_publisher)
        await db.commit()
        await db.refresh(db_publisher)
        return db_publisher
    except IntegrityError as e:
        await db.rollback()
        msg = f"Publisher with name {publisher.name} already exists"
        raise DuplicateEntry(msg) from e


async def get_publisher(db: AsyncSession, publisher_id: int) -> Publisher:
    result = await db.execute(select(Publisher).filter(Publisher.id == publisher_id))
    publisher = result.scalar_one_or_none()
    if not publisher:
        msg = f"Publisher with id {publisher_id} not found"
        raise NoPublisher(msg)
    return publisher


async def get_publishers(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[Publisher]:
    result = await db.execute(select(Publisher).offset(skip).limit(limit))
    publishers = result.scalars().all()
    if not publishers:
        msg = "No publishers found"
        raise NoPublisher(msg)
    return list(publishers)


async def update_publisher(
    db: AsyncSession,
    publisher_id: int,
    publisher: PublisherUpdate,
) -> Publisher:
    db_publisher = await get_publisher(db, publisher_id)

    update_data = publisher.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_publisher, field, value)

    try:
        await db.commit()
        await db.refresh(db_publisher)
        return db_publisher
    except IntegrityError as e:
        await db.rollback()
        msg = f"Publisher with name {publisher.name} already exists"
        raise DuplicateEntry(msg) from e


async def delete_publisher(db: AsyncSession, publisher_id: int) -> None:
    db_publisher = await get_publisher(db, publisher_id)
    await db.delete(db_publisher)
    await db.commit()
