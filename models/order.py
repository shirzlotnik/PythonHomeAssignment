from pydantic import BaseModel, field_validator, Field, WrapValidator
from typing import Annotated, List
from pydantic.v1.class_validators import Validator
from models.commons import validate_timestamp_range


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
    currency: str
    payment_status: str
    items: List[Item]

    @field_validator("payment_status")
    def validate_payment_status(self, payment_status: str) -> str:
        if payment_status not in VALID_PAYMENT_STATUSES:
            raise ValueError(f"Invalid payment status: {payment_status}")
        return payment_status


