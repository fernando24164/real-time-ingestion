from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

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
    except IntegrityError:
        await db.rollback()
        raise DuplicateEntry(f"Publisher with name {publisher.name} already exists")

async def get_publisher(db: AsyncSession, publisher_id: int) -> Publisher:
    result = await db.execute(select(Publisher).filter(Publisher.id == publisher_id))
    publisher = result.scalar_one_or_none()
    if not publisher:
        raise NoPublisher(f"Publisher with id {publisher_id} not found")
    return publisher

async def get_publishers(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Publisher]:
    result = await db.execute(select(Publisher).offset(skip).limit(limit))
    return result.scalars().all()

async def update_publisher(
    db: AsyncSession, publisher_id: int, publisher: PublisherUpdate
) -> Publisher:
    db_publisher = await get_publisher(db, publisher_id)
    
    update_data = publisher.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_publisher, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_publisher)
        return db_publisher
    except IntegrityError:
        await db.rollback()
        raise DuplicateEntry(f"Publisher with name {publisher.name} already exists")

async def delete_publisher(db: AsyncSession, publisher_id: int) -> None:
    db_publisher = await get_publisher(db, publisher_id)
    await db.delete(db_publisher)
    await db.commit()