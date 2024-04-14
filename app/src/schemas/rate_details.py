from datetime import datetime, time, timedelta
from typing import List

from pydantic import BaseModel, Field, UUID4

from .rates import RateModel


class RateDetailModel(BaseModel):
    rate_id: int
    day_of_week: int
    start_time: time
    end_time: time
    hourly_rate: int
    daily_rate: int

    class Config:
        orm_mode = True
