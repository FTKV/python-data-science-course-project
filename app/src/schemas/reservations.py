"""
Module of reservations' schemas
"""

from datetime import datetime
from src.database.models import Status
from pydantic import (
    BaseModel,
    UUID4,
)
from typing import Optional

from src.utils.as_form import as_form


@as_form
class ReservationModel(BaseModel):

    resv_status: Status
    start_date: datetime | None = None
    end_date: datetime | None = None
    user_id: UUID4 | int | None = None
    parking_spot_id: UUID4 | int | None = None
    car_id: UUID4 | int
    rate_id: UUID4 | int


@as_form
class ReservationUpdateModel(BaseModel):
    resv_status: Status | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    debit: float | None = None
    credit: float | None = None
    user_id: UUID4 | int | None = None
    parking_spot_id: UUID4 | int | None = None
    rate_id: UUID4 | int | None = None
