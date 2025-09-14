from app.api.deps import DBSessionDep
from app.schemas.genre import GenreCreate, GenreResponse, GenreUpdate
from app.services.exceptions import DuplicateEntry, NoGenre
from app.services.genre_service import (
    create_genre,
    delete_genre,
    get_genre,
    get_genres,
    update_genre,
)
from fastapi import APIRouter, HTTPException, Query, status

genre_router = APIRouter(prefix="/genres", tags=["Genres"])


@genre_router.post(
    "",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_genre(
    genre: GenreCreate,
    db: DBSessionDep,
) -> GenreResponse:
    try:
        db_genre = await create_genre(db, genre)
        return GenreResponse(
            status="success",
            data=db_genre,
            message="Genre created successfully",
        )
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@genre_router.get("/{genre_id}", response_model=GenreResponse)
async def read_genre(
    genre_id: int,
    db: DBSessionDep,
) -> GenreResponse:
    try:
        db_genre = await get_genre(db, genre_id)
        return GenreResponse(
            status="success",
            data=db_genre,
            message="Genre retrieved successfully",
        )
    except NoGenre as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@genre_router.get("", response_model=list[GenreResponse])
async def read_genres(
    db: DBSessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
) -> list[GenreResponse]:
    genres = await get_genres(db, skip, limit)
    return [
        GenreResponse(
            status="success",
            data=genre,
            message="Genre retrieved successfully",
        )
        for genre in genres
    ]


@genre_router.put("/{genre_id}", response_model=GenreResponse)
async def update_existing_genre(
    genre_id: int,
    genre: GenreUpdate,
    db: DBSessionDep,
) -> GenreResponse:
    try:
        db_genre = await update_genre(db, genre_id, genre)
        return GenreResponse(
            status="success",
            data=db_genre,
            message="Genre updated successfully",
        )
    except NoGenre as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@genre_router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_genre(
    genre_id: int,
    db: DBSessionDep,
) -> None:
    try:
        await delete_genre(db, genre_id)
    except NoGenre as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
