"""
Module of rates' schemas
"""

from typing import List
from pydantic import BaseModel, Field, UUID4, conlist

class RateBase(BaseModel):
    title: str = Field(..., title="Title", max_length=32)
    description: str = Field(None, title="Description", max_length=1024)
    is_daily: bool = Field(False, title="Is Daily")

class RateCreate(RateBase):
    user_id: UUID4

class RateUpdate(RateBase):
    pass

class RateResponse(BaseModel):
    id: UUID4 | int
    title: str = Field(..., title="Title", max_length=32)
    description: str = Field(None, title="Description", max_length=1024)
    is_daily: bool = Field(False, title="Is Daily")
    rate_details: List['RateDetailResponse'] = []

    class Config:
        orm_mode = True

