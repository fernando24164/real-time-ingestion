from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game_store import User
from app.schemas.user import User as UserSchema, UserCreate
from app.schemas.user import UserUpdate
from app.services.exceptions import NoUser


async def create_user(
    postgres_session: AsyncSession, user: UserCreate
) -> Optional[UserSchema]:
    """
    Args:
        postgres_session: The async database session
        user: The user data to create

    Returns:
        UserSchema: The created user data converted to schema
    """
    user_model = User(**user.model_dump())
    postgres_session.add(user_model)
    await postgres_session.commit()
    await postgres_session.refresh(user_model)
    return UserSchema.model_validate(user_model)


async def get_user_by_id(
    user_id: int, postgres_session: AsyncSession
) -> Optional[UserSchema]:
    """
    Args:
        user_id: The ID of the user to retrieve
        postgres_session: The async database session

    Returns:
        UserSchema: The user data converted to schema

    Raises:
        NoUser: If no user is found with the given ID
    """
    query = select(User).where(User.id == user_id)
    result = await postgres_session.execute(query)
    user = result.scalars().first()

    if not user:
        raise NoUser(f"No user found for the customer {user_id}")

    return UserSchema.model_validate(user)


async def get_users(
    postgres_session: AsyncSession, skip: int = 0, limit: int = 100
) -> list[UserSchema]:
    """
    Args:
        postgres_session: The async database session
        skip: The number of records to skip
        limit: The maximum number of records to retrieve

    Returns:
        list[UserSchema]: A list of user data converted to schema
    """
    query = select(User).offset(skip).limit(limit)
    result = await postgres_session.execute(query)
    return [UserSchema.model_validate(user) for user in result.scalars().all()]


async def update_user(
    db: AsyncSession, user_id: int, user: UserUpdate
) -> Optional[UserSchema]:
    db_user = await get_user_by_id(user_id, db)
    for field, value in user.model_dump().items():
        setattr(db_user, field, value)
    await db.commit()
    await db.refresh(db_user)
    return UserSchema.model_validate(db_user)


async def delete_user(db: AsyncSession, user_id: int) -> None:
    db_user = await get_user_by_id(user_id, db)
    await db.delete(db_user)
    await db.commit()
    return None
