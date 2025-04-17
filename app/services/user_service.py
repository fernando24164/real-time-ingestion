from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game_store import User
from app.schemas.user import User as UserSchema
from app.services.exceptions import NoUser


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
