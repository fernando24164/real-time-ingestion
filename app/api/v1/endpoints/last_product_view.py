from fastapi import APIRouter, HTTPException, Query

from app.api.deps import RedisConnectionDep

last_viewed_router = APIRouter(tags=["Last viewed products"])


@last_viewed_router.get("/last_product_viewed", response_model=dict)
async def last_product_view(
    redis_client: RedisConnectionDep,
    customer_id: int = Query(..., description="Customer ID"),
) -> dict:
    """
    Retrieve the last viewed product for a specific customer.
    """
    last_product = await redis_client.get(f"last_viewed:{customer_id}")

    if not last_product:
        raise HTTPException(
            status_code=404,
            detail=f"No last viewed product found for customer {customer_id}",
        )

    return {"last_viewed_product": last_product.decode("utf-8")}
