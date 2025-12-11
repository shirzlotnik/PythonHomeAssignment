from pydantic import BaseModel, Field, model_validator, AfterValidator
from typing import Annotated
from models.commons import validate_timestamp_range


class Chargeback(BaseModel):
    transaction_id: str
    dispute_date: Annotated[str, AfterValidator(validate_timestamp_range)]
    amount: float = Field(..., ge=0)
    currency: str
    reason_code: str
    status: str
    resolution_date: Annotated[str, AfterValidator(validate_timestamp_range)]

    @model_validator(mode="after")
    def validate_dates_range(self):
        if self.dispute_date > self.resolution_date:
            raise ValueError(f"Invalid dates, dispute_date: {self.dispute_date} "
                             f"is after resolution_date: {self.resolution_date}")
        return self
