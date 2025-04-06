from fastapi import APIRouter, HTTPException, Query

from app.api.deps import RedisConnectionDep
from app.services.exceptions import NoLastViewed
from app.services.retrieve_last_viewed import get_last_viewed
from app.schemas.last_viewed import LastViewedProductsResponse

last_viewed_router = APIRouter(tags=["Last viewed products"])


@last_viewed_router.get("/last_product_viewed", response_model=LastViewedProductsResponse)
async def last_product_view(
    redis_client: RedisConnectionDep,
    customer_id: int = Query(..., description="Customer ID"),
) -> LastViewedProductsResponse:
    """
    Retrieve the last viewed products for a specific customer.
    
    Returns a list of product IDs that were last viewed by the customer.
    """
    try:
        products = await get_last_viewed(customer_id, redis_client)
    except NoLastViewed as e:
        raise HTTPException(status_code=204, detail=str(e))

    return LastViewedProductsResponse(
        status="success",
        data=products,
        message="Last viewed products retrieved successfully"
    )
