from pydantic import BaseModel


class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float


class Invoice(BaseModel):
    title: str
    description: str
    items: list[InvoiceItem]

    def get_formatted_csv(self):
        rows = []
        for item in self.items:
            rows.append(
                "\t".join([item.description, "", "", "", str(
                    item.quantity), str(item.unit_price), str(item.amount)])
            )

        return "\n".join(rows)
