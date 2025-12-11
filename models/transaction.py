from pydantic import BaseModel, field_validator, Field, WrapValidator
from typing import Optional, Annotated
from pydantic.v1.class_validators import Validator
from models.commons import validate_timestamp_range

VALID_STATUSES = ["completed", "failed", "pending"]
VALID_PAYMENT_TYPES = ["credit_card", "debit_card", "wallet"]


class PaymentMethod(BaseModel):
    type: str
    provider: str

    @field_validator("type")
    def validate_type(self, payment_type: str) -> str:
        if payment_type not in VALID_PAYMENT_TYPES:
            raise ValueError(f"Invalid transaction status: {payment_type}")
        return payment_type


class Transaction(BaseModel):
    transaction_id: str
    order_id: str
    timestamp: Annotated[str, Validator(validate_timestamp_range)]
    amount: float = Field(..., ge=0)
    currency: str
    status: str
    payment_method: PaymentMethod
    error_code: Optional[str]

    @field_validator("status")
    def validate_status(self, status: str) -> str:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid transaction status: {status}")
        return status


