"""
Module of rates' schemas
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, UUID4

from .rate_details import RateDetailModel

class RateModel(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    description: str
    start_date: datetime
    end_date: datetime
    hourly_rate: int
    daily_rate: int

    rate_details: List[RateDetailModel] = []

    class Config:
        orm_mode = True

class RateResponse(BaseModel):
    id: UUID4 | int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    hourly_rate: int
    daily_rate: int
    rate_details: List[RateDetailModel]
    created_at: datetime
    updated_at: datetime
