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

    def calculate_parking_cost(self, duration: timedelta) -> int:
   
        total_hours = duration.total_seconds() / 3600
        total_days = total_hours / 24

        if duration.total_seconds() < 300:
            return 0  
        else:
            if total_days >= 1:
                return int(total_days * self.daily_rate)
            else:
                return int(total_hours * self.hourly_rate)

    def update_tariff(self, hourly_rate: int, daily_rate: int):
        """Update tariff rates"""
        self.hourly_rate = hourly_rate
        self.daily_rate = daily_rate

    def update_duration(self, start_time: time, end_time: time):
        """Update parking duration"""
        self.start_time = start_time
        self.end_time = end_time

    def update_price(self, hourly_rate: int, daily_rate: int):
        """Update hourly and daily rates"""
        self.hourly_rate = hourly_rate
        self.daily_rate = daily_rate
