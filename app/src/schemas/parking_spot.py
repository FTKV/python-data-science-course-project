"""
Module of parking_spot' schemas
"""


from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict, UUID4

from src.utils.as_form import as_form


@as_form
class ParkingSpotModel(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    description: Annotated[str | None, Field(max_length=1024)] = None
    is_available: bool = True
    is_out_of_service: bool = False


@as_form
class ParkingSpotCreate(ParkingSpotModel):
    pass


@as_form
class ParkingSpotUpdate(ParkingSpotModel):
    title: str = Field(min_length=1, max_length=32)
    is_available: bool = True
    is_out_of_service: bool = False


@as_form
class ParkingSpotDB(ParkingSpotModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    is_available: bool
    is_out_of_service: bool
    user_id: Optional[UUID4 | int]


@as_form
class ParkingSpotResponse(BaseModel):
    user: ParkingSpotDB
    message: str = "Parking Spot Info"
