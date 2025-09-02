from __future__ import annotations
from typing import List, Optional, Callable, Union, Tuple, Dict, cast
from datetime import date, datetime, time, timedelta
from ScheduleDate import ScheduleDate, ScheduleDateBuilder, SpecialScheduleDate
from Show import Show, ShowBuilder
from Episode import Episode, NonEpisode
from Calendar import Calendar
from sortedcontainers import SortedList


class Schedule:
    def __init__(
            self: Schedule,
            special_dates: Optional[List[ScheduleDate]] = None,
            shows: Optional[SortedList] = None) -> None:
        self.special_dates: Dict[date, ScheduleDate] = { special_date.day : special_date for special_date in special_dates } if special_dates else {}
        self.shows: SortedList = shows if shows else SortedList(key=lambda show: show.priority)
        self.empty_shows: List[Show] = []
        self.previous_ep_cache: Dict[Show, datetime] = {}
        self.schedule: Calendar = Calendar()

    def clear_date_range(self: Schedule, start: date, end: Optional[date] = None) -> None:
        if self.schedule.latest_date is None or start > self.schedule.latest_date:
            return
        if start < cast(date, self.schedule.earliest_date):
            start = cast(date, self.schedule.earliest_date)
        if not end:
            end = cast(date, self.schedule.latest_date)

        for day in [start + timedelta(days=i) for i in range((end - start).days + 1)]:
            if day in self.special_dates:
                for slot in (slot for slot in self.special_dates[day].slots if slot.episode):
                    show: Show = self.get_show(cast(Episode, slot.episode).show_name)
                    show.episodes.add(slot.episode)
                    slot.episode = None
                del self.special_dates[day]
        #invalidate cache
        self.previous_ep_cache = {}

    def get_show(self: Schedule, show_name: str) -> Show:
        show = next(entry for entry in self.shows + self.empty_shows if entry.name == show_name)
        return show

    def get_previous_instance_date(self: Schedule, show: Show) -> datetime:
        if show in self.previous_ep_cache:
            return self.previous_ep_cache[show]
        time: Union[datetime, None] = self.find_last_show_appearance(show)
        if time:
            self.previous_ep_cache[show] = time
            return time
        return datetime.min

    def find_last_show_appearance(self: Schedule, show: Show) -> Optional[datetime]:
        if self.schedule.latest_date is None:
            return None
        end_date: date = cast(date, self.schedule.latest_date)
        start_date: date = cast(date, self.schedule.earliest_date)
        for day in [end_date - timedelta(days=i) for i in range((end_date - start_date).days + 1)]:
            if day in self.schedule:
                schedule_date: ScheduleDate = self.schedule[day]
                for slot in schedule_date.slots:
                    if slot.episode and slot.episode.show_name == show.name:
                        return slot.time
        return None

    def collect_next_available_episodes(self: Schedule, slot: datetime) -> SortedList:
        next_episodes: SortedList = SortedList(key=lambda entry: (entry[2], entry[1].priority))
        show: Show
        for show in self.shows:
            last_appearance: datetime = self.get_previous_instance_date(show)
            #use negative distance so that larger distance is lower in value for the sorted list
            distance: timedelta = last_appearance - slot
            if len(show.episodes) == 0:
                next_episodes.add((NonEpisode, show, distance))
            elif cast(Episode, show.episodes[0]).is_available(slot):
                next_episodes.add((show.episodes[0], show, distance))
        return next_episodes

    def get_current_date(self: Schedule, search: date) -> ScheduleDate:
        if search in self.schedule:
            return self.schedule[search]
        new_date: ScheduleDate
        if search in self.special_dates:
            new_date = self.special_dates[search]
        else:
            new_date = cast(ScheduleDate, ScheduleDateBuilder().DefaultDate(search).day)
        return new_date

    def clear_empty_shows(self: Schedule) -> None:
        for reverse_index in range(len(self.shows) - 1, -1, -1):
            empty_show: Show = cast(Show, self.shows[reverse_index])
            if len(empty_show.episodes) == 0:
                del self.shows[reverse_index]
                self.empty_shows.append(empty_show)

    def generate_schedule(self: Schedule, start: date, stop_at_first_empty_show: Optional[bool] = True, end: Optional[date] = None) -> date:
        shift_one_day: timedelta = timedelta(1)
        #start back one day so that the first increment lands on start
        current: date = start - shift_one_day
        keep_going: bool = True
        while keep_going:
            current += shift_one_day
            if end and current > end:
                keep_going = False
                break
            current_date: ScheduleDate = self.get_current_date(current)

            for slot in filter(lambda slot: slot.episode is None, current_date.slots):
                #next_episodes is SortedList[Tuple[Episode, Show, timedelta]]
                next_episodes: SortedList = self.collect_next_available_episodes(slot.time)
                if len(next_episodes) == 0:
                    keep_going = False
                    break
                next_episode: Tuple[Episode, Show, timedelta] = cast(Tuple[Episode, Show, timedelta], next_episodes[0])
                if stop_at_first_empty_show and next_episode[0] is NonEpisode:
                    keep_going = False
                    break
                if keep_going:
                    slot.episode = next_episode[0]
                    self.previous_ep_cache[next_episode[1]] = slot.time
                    next_episode[1].episodes.pop(0)
            self.schedule[current] = current_date
        self.clear_empty_shows()
        return current


class ScheduleBuilder:
    def __init__(self: ScheduleBuilder, schedule: Optional[Schedule] = None):
        self.schedule: Schedule
        if schedule:
            self.schedule = schedule
        else:
            self.schedule = Schedule()

    def RegisterShow(self: ScheduleBuilder, show: Show) -> ScheduleBuilder:
        self.schedule.shows.add(show)
        return self

    def BuildAndRegisterShow(self: ScheduleBuilder, show_generator: Callable[[ShowBuilder]]) -> ScheduleBuilder:
        show_builder: ShowBuilder = ShowBuilder()
        show_generator(show_builder)
        return self.RegisterShow(show_builder.show)

    def RegisterSpecialDate(self: ScheduleBuilder, date_generator: Callable[[ScheduleDateBuilder]]) -> ScheduleBuilder:
        schedule_date_builder: ScheduleDateBuilder = ScheduleDateBuilder()
        date_generator(schedule_date_builder)
        built: ScheduleDate = cast(ScheduleDate, schedule_date_builder.day)
        self.schedule.special_dates[built.day] = built
        return self