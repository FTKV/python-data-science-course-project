from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict, UUID4

from src.utils.as_form import as_form


@as_form
class ParkingSpotModel(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    description: Annotated[str | None, Field(max_length=1024)] = None
    is_available: bool = True
    is_out_of_service: bool = False


class ParkingSpotCreate(ParkingSpotModel):
    pass


class ParkingSpotUpdate(ParkingSpotModel):
    pass


class ParkingSpotDB(ParkingSpotModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    is_available: bool
    is_out_of_service: bool
    user_id: UUID4 | int

class ParkingSpotResponse(BaseModel):
    user: ParkingSpotDB
    message: str = "Parking Spot Info"
