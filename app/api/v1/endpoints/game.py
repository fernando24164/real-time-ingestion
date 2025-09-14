from app.api.deps import DBSessionDep
from app.schemas.game import GameCreate, GameResponse, GameUpdate
from app.services.exceptions import DuplicateEntry, NoGame
from app.services.game_service import (
    create_game,
    delete_game,
    get_game,
    get_games,
    update_game,
)
from fastapi import APIRouter, HTTPException, Query, status

game_router = APIRouter(prefix="/games", tags=["Games"])


@game_router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def create_new_game(
    game: GameCreate,
    db: DBSessionDep,
) -> GameResponse:
    try:
        db_game = await create_game(db, game)
        return GameResponse(
            status="success",
            data=db_game,
            message="Game created successfully",
        )
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@game_router.get("/{game_id}", response_model=GameResponse)
async def read_game(
    game_id: int,
    db: DBSessionDep,
) -> GameResponse:
    try:
        db_game = await get_game(db, game_id)
        return GameResponse(
            status="success",
            data=db_game,
            message="Game retrieved successfully",
        )
    except NoGame as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@game_router.get("", response_model=list[GameResponse])
async def read_games(
    db: DBSessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
) -> list[GameResponse]:
    games = await get_games(db, skip, limit)
    return [
        GameResponse(status="success", data=game, message="Game retrieved successfully")
        for game in games
    ]


@game_router.put("/{game_id}", response_model=GameResponse)
async def update_existing_game(
    game_id: int,
    game: GameUpdate,
    db: DBSessionDep,
) -> GameResponse:
    try:
        db_game = await update_game(db, game_id, game)
        return GameResponse(
            status="success",
            data=db_game,
            message="Game updated successfully",
        )
    except NoGame as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@game_router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_game(
    game_id: int,
    db: DBSessionDep,
) -> None:
    try:
        await delete_game(db, game_id)
    except NoGame as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
