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

class ReservationModel(BaseModel):
    
    resv_status: Optional[Status]
    start_date: datetime
    end_date: Optional[datetime]
    debit: Optional[float]
    credit: Optional[float]
    user_id: UUID4 | int | None = None
    car_id: UUID4 | int | None = None
    rate_id: UUID4 | int 
    
class ReservationUpdateModel(BaseModel):
    resv_status: Optional[Status]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    debit: Optional[float]
    credit: Optional[float]
    user_id: Optional[UUID4]
    car_id: Optional[UUID4]
    rate_id: Optional[UUID4]