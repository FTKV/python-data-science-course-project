"""
Module of rates' schemas
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field, UUID4

from .rate_details import RateDetailModel


class RateModel(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    description: str
    start_date: datetime
    end_date: datetime
    hourly_rate: int
    daily_rate: int


class RateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    hourly_rate: int
    daily_rate: int
    created_at: datetime
    updated_at: datetime
