from __future__ import annotations
from typing import List, Optional, Callable, Union, Tuple, Dict, cast
from datetime import date, datetime, time, timedelta
from ScheduleDate import ScheduleDate, ScheduleDateBuilder, SpecialScheduleDate
from Show import Show, ShowBuilder
from Episode import Episode, NonEpisode
from sortedcontainers import SortedList


class Schedule:
    def __init__(
            self: Schedule,
            special_dates: Optional[List[ScheduleDate]] = None,
            shows: Optional[SortedList] = None) -> None:
        self.special_dates: List[ScheduleDate] = special_dates if special_dates else []
        self.shows: SortedList = shows if shows else SortedList(key=lambda show: show.priority)
        self.schedule: SortedList = SortedList(key=lambda day: day.day)

    def clear_date_range(self: Schedule, start: date, end: Optional[date] = None) -> None:
        if not end:
            end = cast(ScheduleDate, self.schedule[-1]).day
        # iterate in reverse because elements will be removed when encountered
        for i in range(len(self.schedule) - 1, 0, -1):
            date: ScheduleDate = cast(ScheduleDate, self.schedule[i])
            if date.day > end:
                continue
            if date.day < start:
                break
            del self.schedule[i]
            for slot in (slot for slot in date.slots if slot.episode):
                show: Show = self.get_or_create_show(cast(Episode, slot.episode).show_name)
                show.episodes.add(slot.episode)
                slot.episode = None
            if date is SpecialScheduleDate:
                self.special_dates.append(item)

#may become unnecessary if I keep all shows in the schedule and just skip ones with no episodes
    def get_or_create_show(self: Schedule, show_name: str) -> Show:
        show: Show = self.get_show(show_name)
        if not show:
            schedule_generator: ScheduleBuilder = ScheduleBuilder(self)
            schedule_generator.BuildAndRegisterShow(lambda show_builder: show_builder(show_name))
            show = self.get_show(show_name)
        return show

    def get_show(self: Schedule, show_name: str) -> Show:
        show = next(entry for entry in self.shows if entry.name == show_name)
        return show

    #when generating schedule, start by going through existing schedule, incase there are blank dates
    def generate_schedule(self: Schedule, start: date, stop_at_first_empty_show: Optional[bool] = True, end: Optional[date] = None) -> date:
        date_builder: ScheduleDateBuilder = ScheduleDateBuilder()
        previous_ep_cache: Dict[Show, datetime] = {}
        def get_previous_instance_date(show: Show) -> datetime:
            if show in previous_ep_cache:
                return previous_ep_cache[show]
            for i in range(len(self.schedule) - 1, -1, -1):
                check_date: ScheduleDate = cast(ScheduleDate, self.schedule[i])
                for slot in check_date.slots:
                    if slot.episode and slot.episode.show_name == show.name:
                        previous_ep_cache[show] = slot.time
                        return slot.time
            return datetime.min
            
        shift_one_day: timedelta = timedelta(1)
        current: date = start
        keep_going: bool = True
        while keep_going:
            if end and current > end:
                keep_going = False
                break
            utilized_slot: bool = False
            current_date: Union[ScheduleDate, None] = None
            #first see if the day is already in the schedule
            # consider making the schedule a dictionary for easier finding like this... on each "week" cycle, generate the next week of days?
            for i in range(len(self.schedule) - 1, -1, -1):
                check_date: ScheduleDate = cast(ScheduleDate, self.schedule[i])
                if check_date.day == current:
                    utilized_slot = True
                    current_date = check_date
                    break
                elif check_date.day < current:
                    #we've passed the potential location of current
                    break
            if not current_date:
                # is there a better way to manage special dates so that i can remove more easily?  sorted list? peek and if first is the date, pop?
                # what if it is before the current date, also pop until after?
                loc, current_date = next(((i, date) for (i, date) in enumerate(self.special_dates) if date.day == current), (-1, None))
                if current_date:
                    del self.special_dates[loc]
            if not current_date:
                current_date = date_builder.DefaultDate(current).day

            #need to restructure this
            for slot in filter(lambda slot: slot.episode is None, current_date.slots):
                #next_episodes is SortedList[Tuple[Episode, Show, timedelta]]
                next_episodes: SortedList = SortedList(key=lambda entry: (entry[2], entry[1].priority)) # want time to be reverse sort but priority normal sort

                for show in self.shows:
                    last_appearance: datetime = get_previous_instance_date(show)
                    # purposefully make the distance negative so that larger distance is lower in value for the sorted list
                    distance: timedelta = last_appearance - datetime.combine(current, time(0, 0, 0))
                    if stop_at_first_empty_show and len(show.episodes) == 0:
                        next_episodes.add((NonEpisode, show, distance))
                    elif len(show.episodes) > 0 and show.episodes[0].is_available(slot.time):
                        next_episodes.add((show.episodes[0], show, distance))
                if len(next_episodes) == 0:
                    keep_going = False
                    break
                next_episode: Tuple[Episode, Show, timedelta] = cast(Tuple[Episode, Show, timedelta], next_episodes[0])
                if next_episode[0] is NonEpisode:
                    keep_going = False
                    #remove all the empty shows now
                    for reverse_index in range(len(self.shows) - 1, -1, -1):
                        empty_show: Show = cast(Show, self.shows[reverse_index])
                        if len(empty_show.episodes) == 0:
                            del self.shows[reverse_index]
                    #also want to report which show in next_episode[1] is the one that ran out
                    return current #when refactoring: note that I don't want to return +shift_one_day
                    #stop iterating before scheduling the non episode
                    #minorbug: if there is still a slot left in this date, the returned date will be after it... workaround would be to shift back one day before restarting the scheudling process
                    #break
                #pick this episode for this slot
                slot.episode = next_episode[0]
                previous_ep_cache[next_episode[1]] = slot.time
                next_episode[1].episodes.pop(0)
                if not utilized_slot:
                    utilized_slot = True
                    self.schedule.add(current_date)
                    #if there are no slots, also want to append...
            if not current_date.slots:
                self.schedule.add(current_date)

            current += shift_one_day

        #remove all the empty shows now
        for reverse_index in range(len(self.shows) - 1, 0, -1):
            empty_show: Show = self.shows[reverse_index]
            if len(empty_show.episodes) == 0:
                del self.shows[reverse_index]
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
        self.schedule.special_dates.append(cast(ScheduleDate, schedule_date_builder.day))
        return self