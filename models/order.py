from pydantic import BaseModel, AfterValidator
from typing import Annotated, List
from models.commons import validate_timestamp_range, validate_currency

VALID_PAYMENT_STATUSES = ["paid", "failed", "refunded"]


def validate_total_amount(total_amount: str) -> str:
    items_total_amount = sum(item.quantity * item.unit_price for item in self.items)

    if items_total_amount != total_amount:
        raise ValueError("Total amount does not equal to the sum of all the items")


def validate_payment_status(payment_status: str) -> str:
    if payment_status not in VALID_PAYMENT_STATUSES:
        raise ValueError(f"Invalid payment status: {payment_status}")
    return payment_status


class Item(BaseModel):
    product_id: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    order_id: str
    customer_id: str
    timestamp: Annotated[str, AfterValidator(validate_timestamp_range)]
    total_amount: Annotated[float, AfterValidator(validate_total_amount)]
    currency: Annotated[str, AfterValidator(validate_currency)]
    payment_status: Annotated[str, AfterValidator(validate_payment_status)]
    items: List[Item]


