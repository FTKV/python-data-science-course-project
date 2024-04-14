"""
Module of rates' schemas
"""

from typing import List
from pydantic import BaseModel, Field, UUID4, conlist

class RateDetail(BaseModel):
    id: UUID4
    rate_id: UUID4
    detail: str

class Rate(BaseModel):
    id: UUID4
    title: str = Field(..., max_length=32)
    description: Optional[str] = Field(None, max_length=1024)
    is_daily: bool
    user_id: UUID4
    rate_details: List[RateDetail] = []

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
