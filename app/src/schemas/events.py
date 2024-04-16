"""
Module of events' schemas
"""

from datetime import datetime
import json
from typing import Annotated, Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, Field, ConfigDict, UUID4

from src.database.models import Status
from src.utils.as_form import as_form


@as_form
class EventModel(BaseModel):
    parking_spot_id: UUID4 | int | None = None
    reservation_id: UUID4 | int | None = None


@as_form
class EventImageModel(BaseModel):
    plate: Annotated[UploadFile, File()]


class EventDB(EventModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    event_date: datetime
    event_type: Status
    parking_spot_id: UUID4 | int
    reservation_id: UUID4 | int | None = None


# class EventResponse(BaseModel):
#     user: EventDB
#     message: str = "Event Info"
