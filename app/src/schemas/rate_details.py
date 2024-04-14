from datetime import date, time
from typing import Optional
from pydantic import BaseModel, Field, UUID4, ConfigDict

class RateDetailInput(BaseModel):
    start_date: date = Field(..., title="Start Date")
    end_date: date = Field(..., title="End Date")
    start_hour: time = Field(..., title="Start Hour")
    end_hour: time = Field(..., title="End Hour")
    amount: float = Field(..., title="Amount")
    user_id: Optional[UUID4] = Field(None, title="User ID")

    def to_model(self) -> dict:
        return self.dict()

class RateDetailUpdate(BaseModel):
    start_date: Optional[date] = Field(None, title="Start Date")
    end_date: Optional[date] = Field(None, title="End Date")
    start_hour: Optional[time] = Field(None, title="Start Hour")
    end_hour: Optional[time] = Field(None, title="End Hour")
    amount: Optional[float] = Field(None, title="Amount")
    user_id: Optional[UUID4] = Field(None, title="User ID")

    def update_model(self, model: 'RateDetailResponse') -> 'RateDetailResponse':
        update_data = self.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model

class RateDetailResponse(BaseModel):
    id: UUID4 | int
    start_date: date = Field(..., title="Start Date")
    end_date: date = Field(..., title="End Date")
    start_hour: time = Field(..., title="Start Hour")
    end_hour: time = Field(..., title="End Hour")
    amount: float = Field(..., title="Amount")
    user_id: UUID4 | int | None = None

    class Config:
        orm_mode = True

    @classmethod
    def from_model(cls, model) -> 'RateDetailResponse':
        return cls(**model.dict())
