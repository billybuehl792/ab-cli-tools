from pydantic import BaseModel
from decimal import Decimal


class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: Decimal
    amount: Decimal


class Invoice(BaseModel):
    title: str
    description: str
    items: list[InvoiceItem]
