from pydantic import BaseModel, field_validator, Field, model_validator
from typing import Annotated
from pydantic.v1.class_validators import Validator
from models.commons import validate_timestamp_range


class Chargeback(BaseModel):
    transaction_id: str
    dispute_date: Annotated[str, Validator(validate_timestamp_range)]
    amount: float = Field(..., ge=0)
    currency: str
    reason_code: str
    status: str
    resolution_date: Annotated[str, Validator(validate_timestamp_range)]

    @model_validator(mode="after")
    def validate_dates_range(self):
        if self.dispute_date > self.resolution_date:
            raise ValueError(f"Invalid dates, dispute_date: {self.dispute_date} "
                             f"is after resolution_date: {self.resolution_date}")
        return self
