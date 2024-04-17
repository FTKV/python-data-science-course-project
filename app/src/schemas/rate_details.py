from datetime import date, time
from typing import Optional
from pydantic import BaseModel, Field, UUID4, ConfigDict

from src.utils.as_form import as_form


@as_form
class RateDetailModel(BaseModel):
    start_date: date = Field(..., title="Start Date")
    end_date: date = Field(..., title="End Date")
    start_hour: time = Field(..., title="Start Hour")
    end_hour: time = Field(..., title="End Hour")
    amount: float = Field(..., title="Amount")


@as_form
class RateDetailUpdate(BaseModel):
    start_date: Optional[date] = Field(None, title="Start Date")
    end_date: Optional[date] = Field(None, title="End Date")
    start_hour: Optional[time] = Field(None, title="Start Hour")
    end_hour: Optional[time] = Field(None, title="End Hour")
    amount: Optional[float] = Field(None, title="Amount")
    user_id: UUID4 | int | None = None


class RateDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    start_date: date = Field(..., title="Start Date")
    end_date: date = Field(..., title="End Date")
    start_hour: time = Field(..., title="Start Hour")
    end_hour: time = Field(..., title="End Hour")
    amount: float = Field(..., title="Amount")
    user_id: UUID4 | int | None = None
