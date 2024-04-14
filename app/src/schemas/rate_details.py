from datetime import datetime, time, timedelta
from typing import List

from pydantic import BaseModel, Field, UUID4
from apscheduler.schedulers.background import BackgroundScheduler

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

    def get_applicable_rate(self, current_time: time) -> int:
        """Get applicable rate based on the current time"""
        if self.start_time <= current_time < self.end_time:
            return self.hourly_rate
        else:
            return 0

    def get_current_rate(self) -> int:
        """Get the current rate for the parking"""
        return self.hourly_rate  # Return the current hourly rate
