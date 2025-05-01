from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game_store import Game
from app.schemas.game import GameCreate, GameInDB, GameUpdate
from app.services.exceptions import NoGame


async def create_game(db: AsyncSession, game: GameCreate) -> GameInDB:
    db_game = Game(**game.model_dump())
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return GameInDB(**db_game.model_dump())


async def get_game(db: AsyncSession, game_id: int) -> GameInDB:
    result = await db.execute(select(Game).filter(Game.id == game_id))
    game = result.scalar_one_or_none()
    if not game:
        raise NoGame(f"Game with id {game_id} not found")
    return GameInDB(**game.model_dump())


async def get_games(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[GameInDB]:
    result = await db.execute(select(Game).offset(skip).limit(limit))
    return [GameInDB(**game.model_dump()) for game in result.scalars().all()]


async def update_game(db: AsyncSession, game_id: int, game: GameUpdate) -> GameInDB:
    db_game = await get_game(db, game_id)
    for field, value in game.model_dump().items():
        setattr(db_game, field, value)
    await db.commit()
    await db.refresh(db_game)
    return GameInDB(**db_game.model_dump())


async def delete_game(db: AsyncSession, game_id: int) -> None:
    db_game = await get_game(db, game_id)
    await db.delete(db_game)
    await db.commit()
