from fastapi import APIRouter, HTTPException, Query, status
from typing import List

from app.api.deps import DBSessionDep
from app.schemas.publisher import PublisherCreate, PublisherUpdate, PublisherResponse
from app.services.exceptions import NoPublisher, DuplicateEntry
from app.services.publisher_service import (
    create_publisher,
    get_publisher,
    get_publishers,
    update_publisher,
    delete_publisher,
)

publisher_router = APIRouter(prefix="/publishers", tags=["Publishers"])

@publisher_router.post("", response_model=PublisherResponse, status_code=status.HTTP_201_CREATED)
async def create_new_publisher(
    publisher: PublisherCreate,
    db: DBSessionDep,
) -> PublisherResponse:
    try:
        db_publisher = await create_publisher(db, publisher)
        return PublisherResponse(
            status="success",
            data=db_publisher,
            message="Publisher created successfully"
        )
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e))

@publisher_router.get("/{publisher_id}", response_model=PublisherResponse)
async def read_publisher(
    publisher_id: int,
    db: DBSessionDep,
) -> PublisherResponse:
    try:
        db_publisher = await get_publisher(db, publisher_id)
        return PublisherResponse(
            status="success",
            data=db_publisher,
            message="Publisher retrieved successfully"
        )
    except NoPublisher as e:
        raise HTTPException(status_code=404, detail=str(e))

@publisher_router.get("", response_model=List[PublisherResponse])
async def read_publishers(
    db: DBSessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
) -> List[PublisherResponse]:
    publishers = await get_publishers(db, skip, limit)
    return [
        PublisherResponse(
            status="success",
            data=publisher,
            message="Publisher retrieved successfully"
        )
        for publisher in publishers
    ]

@publisher_router.put("/{publisher_id}", response_model=PublisherResponse)
async def update_existing_publisher(
    publisher_id: int,
    publisher: PublisherUpdate,
    db: DBSessionDep,
) -> PublisherResponse:
    try:
        db_publisher = await update_publisher(db, publisher_id, publisher)
        return PublisherResponse(
            status="success",
            data=db_publisher,
            message="Publisher updated successfully"
        )
    except NoPublisher as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateEntry as e:
        raise HTTPException(status_code=400, detail=str(e))

@publisher_router.delete("/{publisher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_publisher(
    publisher_id: int,
    db: DBSessionDep,
) -> None:
    try:
        await delete_publisher(db, publisher_id)
    except NoPublisher as e:
        raise HTTPException(status_code=404, detail=str(e))