from __future__ import annotations
from typing import List, Union, Optional
from datetime import date, datetime, time
from ShowSlot import ShowSlot

class ScheduleDate:
    def __init__(
            self: ScheduleDate,
            day: date,
            slots: Optional[List[ShowSlot]] = None,
            special_notes: Optional[List[str]] = None) -> None:
        self.day: date = day
        self.slots: List[ShowSlot] = slots if slots else []
        self.special_notes: List[str] = special_notes if special_notes else []


def ScheduleDateKey(day: ScheduleDate) -> date:
    return day.day


class DefaultScheduleDate(ScheduleDate):
    def __init__(self: DefaultScheduleDate, day: date) -> None:
        super().__init__(day)


class SpecialScheduleDate(ScheduleDate):
    def __init__(self: SpecialScheduleDate, day: date) -> None:
        super().__init__(day)


class ScheduleDateBuilder:
    def __init__(self: ScheduleDateBuilder, sched_date: Optional[ScheduleDate] = None):
        self.day: Union[ScheduleDate, None] = sched_date

    def SpecialDate(self: ScheduleDateBuilder, day: date) -> ScheduleDateBuilder:
        self.day = SpecialScheduleDate(day)
        return self

    def DefaultDate(self: ScheduleDateBuilder, day: date) -> ScheduleDateBuilder:
        self.day = DefaultScheduleDate(day)
        if day.weekday() == 5 or day.weekday() == 6:
            self.WithLunchSlot()
        self.WithDinnerSlot()
        return self

    def WithLunchSlot(self: ScheduleDateBuilder) -> ScheduleDateBuilder:
        return self.WithSlot(time(12))

    def WithDinnerSlot(self: ScheduleDateBuilder) -> ScheduleDateBuilder:
        return self.WithSlot(time(18))

    def WithSlot(self: ScheduleDateBuilder, time: time) -> ScheduleDateBuilder:
        self.day.slots.append(ShowSlot(datetime.combine(self.day.day, time)))
        return self

    #should be only for special dates...
    def WithNote(self: ScheduleDateBuilder, note: str) -> ScheduleDateBuilder:
        self.day.special_notes.append(note)
        return self
