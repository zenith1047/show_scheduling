from __future__ import annotations
from typing import Dict, Union
from datetime import date, timedelta
from ScheduleDate import ScheduleDate

class Calendar:
    @staticmethod
    # date.weekday() but with sunday = 0 instead of 6
    def sunday_first_weekday(date: date) -> int:
        return (date.weekday() + 1) % 7

    def __init__(self: Calendar) -> None:
        self.calendar: Dict[date, ScheduleDate] = {}
        self.latest_date: Union[date, None] = None
        self.earliest_date: Union[date, None] = None

    def __getitem__(self: Calendar, day: date) -> ScheduleDate:
        return self.calendar[day]

    def __setitem__(self: Calendar, day: date, schedule_date: ScheduleDate) -> None:
        self.calendar[day] = schedule_date
        if not self.earliest_date or day < self.earliest_date:
            self.earliest_date = day
        if not self.latest_date or day > self.latest_date:
            self.latest_date = day

    def __contains__(self: Calendar, day: date) -> bool:
        return day in self.calendar

    def earliest_sunday(self: Calendar) -> Union[date, None]:
        if not self.earliest_date:
            return None
        days_to_subtract = Calendar.sunday_first_weekday(self.earliest_date)
        return self.earliest_date - timedelta(days=days_to_subtract)

    def latest_saturday(self: Calendar) -> Union[date, None]:
        if not self.latest_date:
            return None
        days_to_add = (6 - Calendar.sunday_first_weekday(self.latest_date))
        return self.latest_date + timedelta(days=days_to_add)