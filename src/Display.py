from __future__ import annotations
from typing import List, Optional, Set, Iterable, cast
from datetime import date, timedelta
from ScheduleDate import ScheduleDate
from Schedule import Schedule
from Show import Show
from Episode import Episode


MAX_PRINT_DAY_ROWS: int = 5
DAYS_IN_WEEK: int = 7

class PrintDay:
    def __init__(self: PrintDay, date: date) -> None:
        self.day = date
        self.rows: List[str] = [""] * MAX_PRINT_DAY_ROWS
        self.rows[0] = date.strftime("%b %d")

    def max_length(self: PrintDay) -> int:
        return max(len(row) for row in self.rows)


class PrintWeek:
    def __init__(self: PrintWeek, days: Optional[List[PrintDay]] = None) -> None:
        self.days: List[PrintDay]
        if days:
            self.days = days
        else:
            self.days = []

    def to_string(self: PrintWeek, day_widths: List[int]) -> str:
        pretty: List[str] = [""] * MAX_PRINT_DAY_ROWS
        for row in range(0, MAX_PRINT_DAY_ROWS):
            week: List[str] = [""] * DAYS_IN_WEEK
            for i, day in enumerate(self.days):
                week[i] = day.rows[row].ljust(day_widths[i])
            pretty[row] = " | ".join(week)
        return "\n".join(pretty)

    def to_csv(self: PrintWeek, separator: str = ",") -> str:
        csv: List[str] = [""] * MAX_PRINT_DAY_ROWS
        for row in range(0, MAX_PRINT_DAY_ROWS):
            csv[row] = separator.join(day.rows[row] for day in self.days)
        return "\n".join(csv)


# date.weekday() but with sunday = 0 instead of 6
def sunday_first_weekday(date: date) -> int:
    return (date.weekday() + 1) % 7


def pad_week(week: PrintWeek, start_date: date, num_pad: int):
    for i in range(0, num_pad):
        week.days.append(PrintDay(start_date + timedelta(days=i)))


def to_print_weeks(schedule: Schedule) -> List[PrintWeek]:
    print_weeks: List[PrintWeek] = []
    schedule_date: ScheduleDate = cast(ScheduleDate, schedule.schedule[0])
    days_back: int = sunday_first_weekday(schedule_date.day)
    curr_week: PrintWeek = PrintWeek()
    #pad front so that we start on a sunday
    pad_week(curr_week, schedule_date.day - timedelta(days=days_back), days_back)

    for schedule_date in schedule.schedule:
        if len(curr_week.days) == DAYS_IN_WEEK:
            print_weeks.append(curr_week)
            curr_week = PrintWeek()
        print_day: PrintDay = PrintDay(schedule_date.day)
        for i, slot in enumerate((slot for slot in schedule_date.slots)):
            if slot.episode:
                print_day.rows[i + 1] = slot.episode.display_name()
        if schedule_date.special_notes:
            print_day.rows[4] = "; ".join(schedule_date.special_notes)
        curr_week.days.append(print_day)

    #collect items in groups of seven
    print_date: PrintDay = curr_week.days[-1]
    days_left: int = 6 - sunday_first_weekday(print_date.day)
    #pad back to end on a saturday
    pad_week(curr_week, print_date.day + timedelta(days=1), days_left)
    print_weeks.append(curr_week)
    return print_weeks


def schedule_to_string(schedule: Schedule) -> str:
    print_weeks: List[PrintWeek] = to_print_weeks(schedule)
    max_col_widths: List[int] = [0] * 7
    for day in range(0, DAYS_IN_WEEK):
        max_col_widths[day] = max(week.days[day].max_length() for week in print_weeks)

    pretty: List[str] = list(week.to_string(max_col_widths) for week in print_weeks)
    length: int = pretty[0].index('\n')
    spacer: str = "\n" + "-" * length + "\n"
    return spacer.join(pretty)

def schedule_to_csv(schedule: Schedule, separator: str = ",") -> str:
    print_weeks: List[PrintWeek] = to_print_weeks(schedule)
    pretty: List[str] = [week.to_csv(separator) for week in print_weeks]
    return "\n".join(pretty)

def schedule_to_tab_delimited(schedule: Schedule) -> str:
    return schedule_to_csv(schedule, "\t")

def schedule_episode_pool(schedule: Schedule) -> str:
    pretty: str = ""
    show: Show
    episodes_list: List[str] = []
    for show in schedule.shows:
        episode: Episode
        episodes_list.append("\n".join(episode.display_name() for episode in show.episodes))

    return "\n".join(episodes_list)


#this won't work beecause i've been deleting shows from the dict as i add them to the schedule
#keep an alias pointer to the show in the episodes? cyclic...
#hvae schedule just move between all shows and available shows...
#have schedule keep all shows present but skip over ones with no episodes?
#def order_show_names_by_show_color(show_names: Iterable[str], shows: dict[str, Show]) -> List[str]:
    #pass


def schedule_paste_format(schedule: Schedule, pending_shows: Iterable[Show]) -> str:
    weeks_display: List[str] = schedule_to_csv(schedule).split("\n")
    remaining_episodes_display: List[str] = schedule_episode_pool(schedule).split("\n")
    pending_episodes: List[str] = [ep.display_name() for show in pending_shows for ep in show.episodes]
    remaining_episodes_display += pending_episodes
    shows_set: Set[str] = set()
    for day in schedule.schedule:
        for slot in day.slots:
            if slot.episode:
                shows_set.add(slot.episode.show_name)

    shows_display: List[str] = list(shows_set)
    shows_display.sort()

    max_shows: int = 15
    if len(shows_display) < max_shows:
        for i in range(len(shows_display), max_shows):
            shows_display.append("." * i)

    longest_list = max((len(weeks_display), len(shows_display), len(remaining_episodes_display)))

    formatted: List[str] = [""] * longest_list
    for i in range(0, longest_list):
        if i < len(weeks_display):
            formatted[i] += weeks_display[i]
        else:
            formatted[i] += "," * weeks_display[0].count(",")

        if i < len(remaining_episodes_display):
            formatted[i] += ",," + remaining_episodes_display[i]
        elif i < len(shows_display):
            formatted[i] += ",,"

        if i < len(shows_display):
            formatted[i] += ",," + shows_display[i]

    return "\n".join(formatted)