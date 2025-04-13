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
    customer_id: int = Query(..., description="Customer ID", gt=0),
) -> UserResponse:
    """
    Retrieve the user information for a specific customer.

    Args:
        postgres_session: Database session dependency
        customer_id: The unique identifier of the customer

    Returns:
        UserResponse: The user information

    Raises:
        HTTPException: If the user is not found (404)
    """
    try:
        user = await get_user_by_id(customer_id, postgres_session)
    except NoUser as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {customer_id} not found",
        )

    return UserResponse(
        status="success", data=user, message="User retrieved successfully"
    )
