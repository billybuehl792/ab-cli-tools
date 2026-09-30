import subprocess

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

    def copy_items_to_clipboard(self):
        rows = []
        for item in self.items:
            rows.append(
                "\t".join([item.description, "", "", "", str(
                    item.quantity), str(item.unit_price), str(item.amount)])
            )

        subprocess.run(["pbcopy"], input="\n".join(rows), text=True)
        print("Invoice item rows copied to clipboard!")
