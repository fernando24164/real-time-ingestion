from fastapi import APIRouter, HTTPException, Query

from app.api.deps import DBSessionDep
from app.schemas.user import User
from app.services.exceptions import NoUser
from app.services.user_service import get_user_by_id

user_router = APIRouter(tags=["User"])


@user_router.get("/user", response_model=User)
async def user(
    postgres_session: DBSessionDep,
    customer_id: int = Query(..., description="Customer ID"),
) -> User:
    """
    Retrieve the user information for a specific customer.
    """
    try:
        user = await get_user_by_id(customer_id, postgres_session)
        return user
    except NoUser as e:
        raise HTTPException(status_code=204, detail=str(e))
