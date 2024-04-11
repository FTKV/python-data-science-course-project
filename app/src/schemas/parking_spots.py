"""
Module of parking_spot' schemas
"""

from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict, UUID4


class ParkingSpotModel(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    description: Annotated[str | None, Field(max_length=1024)] = None


class ParkingSpotUpdate(ParkingSpotModel):
    title: Annotated[str | None, Field(min_length=1, max_length=32)] = None
    description: Annotated[str | None, Field(max_length=1024)] = None


class ParkingSpotDB(ParkingSpotModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    is_available: bool
    is_out_of_service: bool
    created_at: datetime
    updated_at: datetime


class ParkingSpotResponse(BaseModel):
    user: ParkingSpotDB
    message: str = "Parking Spot Info"
