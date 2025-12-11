from pydantic import BaseModel, field_validator, Field, WrapValidator, AfterValidator
from typing import Optional, Annotated, Any
from models.commons import validate_timestamp_range, validate_currency

VALID_STATUSES = ["completed", "failed", "pending"]
VALID_PAYMENT_TYPES = ["credit_card", "debit_card", "wallet"]


def validate_status(status: str) -> str:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid transaction status: {status}")
    return status


def validate_type(payment_type: str) -> str:
    if payment_type not in VALID_PAYMENT_TYPES:
        raise ValueError(f"Invalid transaction status: {payment_type}")
    return payment_type


class PaymentMethod(BaseModel):
    type: Annotated[str, AfterValidator(validate_type)]
    provider: str


class Transaction(BaseModel):
    transaction_id: str
    order_id: str
    timestamp: Annotated[Any, AfterValidator(validate_timestamp_range)]
    amount: float = Field(..., ge=0)
    currency: Annotated[str, AfterValidator(validate_currency)]
    status: Annotated[str, AfterValidator(validate_status)]
    payment_method: PaymentMethod
    error_code: Optional[str] = None



