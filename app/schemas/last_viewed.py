from typing import List

from pydantic import BaseModel

from app.schemas.response_base import ResponseBase


class LastViewedProducts(BaseModel):
    last_viewed_products: List[str]


class LastViewedProductsResponse(ResponseBase[LastViewedProducts]):
    pass
