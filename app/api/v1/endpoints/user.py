from app.api.deps import DBSessionDep
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.exceptions import DuplicateEntry, NoUser
from app.services.user_service import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from fastapi import APIRouter, HTTPException, Query, status

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserCreate,
    db: DBSessionDep,
) -> UserResponse:
    try:
        db_user = await create_user(db, user)
        return UserResponse(
            status="success",
            data=db_user,
            message="User created successfully",
        )
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@user_router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: DBSessionDep,
) -> UserResponse:
    try:
        user = await get_user_by_id(user_id, db)
        return UserResponse(
            status="success",
            data=user,
            message="User retrieved successfully",
        )
    except NoUser as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        ) from e


@user_router.get("", response_model=list[UserResponse])
async def read_users(
    db: DBSessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
) -> list[UserResponse]:
    users = await get_users(db, skip, limit)
    return [
        UserResponse(status="success", data=user, message="User retrieved successfully")
        for user in users
    ]


@user_router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: int,
    user: UserUpdate,
    db: DBSessionDep,
) -> UserResponse:
    try:
        db_user = await update_user(db, user_id, user)
        return UserResponse(
            status="success",
            data=db_user,
            message="User updated successfully",
        )
    except NoUser as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(
    user_id: int,
    db: DBSessionDep,
) -> None:
    try:
        await delete_user(db, user_id)
    except NoUser as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
