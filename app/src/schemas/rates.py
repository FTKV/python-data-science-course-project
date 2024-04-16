"""
Module of rates' schemas
"""

from typing import List
from pydantic import BaseModel, Field, UUID4, ConfigDict
from typing import Optional

from src.schemas.rate_details import RateDetailResponse


class RateBase(BaseModel):
    title: str = Field(..., title="Title", min_length=2, max_length=32)
    description: str = Field(None, title="Description", max_length=1024)
    is_daily: bool = Field(False, title="Is Daily")


class RateCreate(RateBase):
    user_id: UUID4 | int | None = None


class RateUpdate(BaseModel):
    title: Optional[str] = Field(None, title="Title", min_length=2, max_length=32)
    description: Optional[str] = Field(None, title="Description", max_length=1024)
    is_daily: Optional[bool] = Field(None, title="Is Daily")


class RateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    title: str = Field(..., title="Title", min_length=2, max_length=32)
    description: str = Field(None, title="Description", max_length=1024)
    is_daily: bool = Field(False, title="Is Daily")


class RateDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    title: str = Field(..., title="Title", min_length=2, max_length=32)
    description: str = Field(None, title="Description", max_length=1024)
    is_daily: bool = Field(False, title="Is Daily")
    rate_details: List[RateDetailResponse] = []
