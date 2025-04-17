from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DBSessionDep
from app.schemas.user import UserResponse
from app.services.exceptions import NoUser
from app.services.user_service import get_user_by_id

user_router = APIRouter(tags=["User"])


@user_router.get(
    "/user",
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {"description": "User found"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_user(
    postgres_session: DBSessionDep,
    user_id: int = Query(..., description="User ID", gt=0),
) -> UserResponse:
    """
    Retrieve the user information for a specific user.

    Args:
        postgres_session: Database session dependency
        user_id: The unique identifier of the user

    Returns:
        UserResponse: The user information

    Raises:
        HTTPException: If the user is not found (404)
    """
    try:
        user = await get_user_by_id(user_id, postgres_session)
    except NoUser as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    return UserResponse(
        status="success", data=user, message="User retrieved successfully"
    )
