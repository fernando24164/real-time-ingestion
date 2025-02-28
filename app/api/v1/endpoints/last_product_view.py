from fastapi import APIRouter, HTTPException, Query

from app.api.deps import RedisConnectionDep
from app.services.exceptions import NoLastViewed
from app.services.retrieve_last_viewed import get_last_viewed

last_viewed_router = APIRouter(tags=["Last viewed products"])


@last_viewed_router.get("/last_product_viewed", response_model=dict)
async def last_product_view(
    redis_client: RedisConnectionDep,
    customer_id: int = Query(..., description="Customer ID"),
) -> dict:
    """
    Retrieve the last viewed product for a specific customer.
    """
    try:
        products = await get_last_viewed(customer_id, redis_client)
    except NoLastViewed as e:
        raise HTTPException(status_code=204, detail=str(e))

    return products
