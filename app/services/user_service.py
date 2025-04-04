from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.web_event import User
from app.services.exceptions import NoUser


async def get_user_by_id(
    customer_id: int, postgres_session: AsyncSession
) -> Optional[User]:
    """
    Args:
        customer_id: The ID of the user to retrieve
        postgres_session: The async database session

    Returns:
        UserSchema: The user data converted to schema

    Raises:
        NoUser: If no user is found with the given ID
    """
    query = select(User).where(User.id == customer_id)
    result = await postgres_session.execute(query)
    user = result.scalars().first()

    if not user:
        raise NoUser(f"No user found for the customer {customer_id}")

    return user
