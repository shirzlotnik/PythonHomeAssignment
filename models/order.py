from pydantic import BaseModel, field_validator, Field, WrapValidator
from typing import Annotated, List
from pydantic.v1.class_validators import Validator
from models.commons import validate_timestamp_range, validate_currency

VALID_PAYMENT_STATUSES = ["paid", "failed", "refunded"]


class Item(BaseModel):
    product_id: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    order_id: str
    customer_id: str
    timestamp: Annotated[str, Validator(validate_timestamp_range)]
    total_amount: float = Field(..., ge=0)
    currency: Annotated[str, Validator(validate_currency)]
    payment_status: str
    items: List[Item]

    @field_validator("payment_status")
    def validate_payment_status(self, payment_status: str) -> str:
        if payment_status not in VALID_PAYMENT_STATUSES:
            raise ValueError(f"Invalid payment status: {payment_status}")
        return payment_status

    @field_validator("total_amount")
    def validate_total_amount(self, total_amount: str) -> str:
        items_total_amount = sum(item.quantity * item.unit_price for item in self.items)

        if items_total_amount != total_amount:
            raise ValueError("Total amount does not equal to the sum of all the items")



