from decimal import Decimal
from pydantic import BaseModel, Field


class Price(BaseModel):
    description: str
    unit: str
    unit_size: Decimal = Field(ge=0)
    unit_price: Decimal = Field(ge=0)
