"""
Module of events' schemas
"""

from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict, UUID4

from src.database.models import Status

class EventModel(BaseModel):
    event_type: Status
    parking_spot_id: UUID4 | int
    reservation_id: UUID4 | int
    

class EventDB(EventModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    event_date: datetime
    event_type: Status
    parking_spot_id: UUID4 | int
    reservation_id: UUID4 | int


# class EventResponse(BaseModel):
#     user: EventDB
#     message: str = "Event Info"
