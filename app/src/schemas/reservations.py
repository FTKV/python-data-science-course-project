"""
Module of reservations' schemas
"""


from datetime import datetime
from src.database.models import Status
from pydantic import (
    BaseModel,
    UUID4,
)
from typing import Optional, Union

class ReservationModel(BaseModel):
    
    resv_status: Optional[Status]
    start_date: datetime
    end_date: Optional[datetime]
    debit: Optional[float]
    credit: Optional[float]
    user_id: Optional[Union[UUID4, int]]
    car_id: Union[UUID4, int]
    rate_id: Union[UUID4, int]
    
class ReservationUpdateModel(BaseModel):
    resv_status: Optional[Status]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    debit: Optional[float]
    credit: Optional[float]
    user_id: Optional[Union[UUID4, int]]
    car_id: Optional[Union[UUID4, int]]
    rate_id: Optional[Union[UUID4, int]]