from typing import Iterable, Callable
from datetime import date, datetime
from Schedule import Schedule, ScheduleBuilder
from Show import Show, ShowBuilder
from SortedList import SortedList
import Display


def add_show_to_pool(pool: dict[str, Show], name: str, config: Callable[[ShowBuilder], ShowBuilder]) -> None:
    builder: ShowBuilder = ShowBuilder()
    builder.CreateShow(name)
    config(builder)
    builder.WithPriority(len(pool) + 1)
    if builder.show:
        pool[name] = builder.show


def build_show_pool() -> dict[str, Show]:
    pool: dict[str, Show] = {}
    add_show_to_pool(pool, "The Night Manager", lambda builder: builder
                     .WithEpisodes(num_episodes=6, start_episode=2))
    add_show_to_pool(pool, "Dept Q", lambda builder: builder
                     .WithEpisodes(num_episodes=9, start_episode=8))
    add_show_to_pool(pool, "Penny Dreadful S2", lambda builder: builder
                     .WithEpisodes(num_episodes=10, start_episode=4))
    add_show_to_pool(pool, "Nautilus", lambda builder: builder
                     .WithEpisode(lambda ep: ep.CreateEpisode(8, "Nautilus").AvailableAt(datetime(2025, 8, 10, 21))) 
                     .WithEpisode(lambda ep: ep.CreateEpisode(9, "Nautilus").AvailableAt(datetime(2025, 8, 17, 21))) 
                     .WithEpisode(lambda ep: ep.CreateEpisode(10, "Nautilus").AvailableAt(datetime(2025, 8, 17, 21))) 
                     .FinalizeLastEpisode())
    add_show_to_pool(pool, "Peacemaker S2", lambda builder: builder
                     .WithWeeklyEpisodes(datetime(2025, 8, 21, 21), 8))
    add_show_to_pool(pool, "Murderbot", lambda builder: builder
                     .WithEpisodes(num_episodes=10))
    add_show_to_pool(pool, "Buccaneers S2", lambda builder: builder
                     .WithEpisodes(num_episodes=8))
    add_show_to_pool(pool, "Foundation S3", lambda builder: builder
                     .WithEpisodes(num_episodes=10))
    add_show_to_pool(pool, "Penny Dreadful S3", lambda builder: builder
                     .WithEpisodes(num_episodes=9))
    add_show_to_pool(pool, "Slow Horses S5", lambda builder: builder
                     .WithWeeklyEpisodes(start_date=datetime(2025, 9, 24), num_episodes=6))
    add_show_to_pool(pool, "Dickinson S1", lambda builder: builder
                     .WithEpisodes(num_episodes=10))
    add_show_to_pool(pool, "Your Friends & Neighbors", lambda builder: builder
                     .WithEpisodes(num_episodes=9))
    add_show_to_pool(pool, "Chief of War", lambda builder: builder
                     .WithEpisodes(num_episodes=9))
    add_show_to_pool(pool, "Gen V S2", lambda builder: builder
                     .WithEpisode(lambda ep: ep.CreateEpisode(1, "Gen V S2").AvailableAt(datetime(2025, 9, 17)))
                     .WithEpisode(lambda ep: ep.CreateEpisode(2, "Gen V S2").AvailableAt(datetime(2025, 9, 17)))
                     .WithEpisode(lambda ep: ep.CreateEpisode(3, "Gen V S2").AvailableAt(datetime(2025, 9, 17)))
                     .WithWeeklyEpisodes(start_date=datetime(2025, 9, 24), num_episodes=8, start_episode=4))
    add_show_to_pool(pool, "The Talamasca", lambda builder: builder
                     .WithWeeklyEpisodes(start_date=datetime(2025, 10, 26, 21), num_episodes=6))
    add_show_to_pool(pool, "Downton Abbey S1", lambda builder: builder
                     .WithEpisodes(num_episodes=7))
    add_show_to_pool(pool, "Alien: Earth", lambda builder: builder
                     .WithEpisodes(num_episodes=8))
    add_show_to_pool(pool, "Only Murders in the Building S5", lambda builder: builder
                     .WithEpisodes(num_episodes=10))
    return pool

def build_schedule() -> Schedule:
    builder: ScheduleBuilder = ScheduleBuilder()
    builder.CreateSchedule()

    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 8, 9))
                                .WithDinnerSlot()
                                .WithNote("BOSTON"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 8, 24))
                                .WithLunchSlot()
                                .WithDinnerSlot()
                                .WithNote("start AppleTV+ trial on prime"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 8, 30))
                                .WithLunchSlot()
                                .WithNote("HARRISON BIRTHDAY"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 9, 1))
                                .WithLunchSlot()
                                .WithDinnerSlot()
                                .WithNote("LABOR DAY"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 8, 24))
                                .WithLunchSlot()
                                .WithDinnerSlot()
                                .WithNote("AppleTV+ trial on Prime"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 9, 30))
                                .WithNote("HAMILTON"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 10, 1))
                                .WithLunchSlot()
                                .WithDinnerSlot()
                                .WithNote("DAY AFTER HAMILTON"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 10, 13))
                                .WithLunchSlot()
                                .WithDinnerSlot()
                                .WithNote("INDIGENOUS PEOPLE'S DAY"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 10, 30))
                                .WithDinnerSlot()
                                .WithNote("Cancel AppleTV+ on Prime"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 11, 2))
                                .WithLunchSlot()
                                .WithNote("SAM ASME, tentative"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 11, 3))
                                .WithNote("SAM ASME"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 11, 4))
                                .WithNote("SAM ASME"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 11, 5))
                                .WithNote("SAM ASME"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 11, 6))
                                .WithNote("SAM ASME"))
    builder.RegisterSpecialDate(lambda builder: builder
                                .SpecialDate(date(2025, 11, 7))
                                .WithDinnerSlot()
                                .WithNote("SAM ASME, tentative"))
    if builder.schedule:
        return builder.schedule
    return Schedule()


def register_shows(schedule: Schedule, shows: Iterable[Show]) -> None:
    builder: ScheduleBuilder = ScheduleBuilder(schedule)
    for show in shows:
        builder.RegisterShow(show)


if __name__ == '__main__':
    #make this into a jupyter notebook for ease of on-the-fly script modification more like interactive workflow
    schedule: Schedule = build_schedule()
    shows: dict[str, Show] = build_show_pool()

    register_shows(schedule, [shows["The Night Manager"], shows["Dept Q"], shows["Penny Dreadful S2"], shows["Nautilus"], shows["Peacemaker S2"]])
    del shows["The Night Manager"]
    del shows["Dept Q"]
    del shows["Penny Dreadful S2"]
    del shows["Nautilus"]
    del shows["Peacemaker S2"]
    stopped: date = schedule.generate_schedule(start=date(2025, 8, 13), stop_at_first_empty_show=False, end=date(2025, 8, 23))
    #print(Display.schedule_to_string(schedule)) 

    register_shows(schedule, [shows["Murderbot"], shows["Buccaneers S2"], shows["Foundation S3"]])
    del shows["Murderbot"]
    del shows["Buccaneers S2"]
    del shows["Foundation S3"]
    stopped = schedule.generate_schedule(start=stopped)
    stopped = schedule.generate_schedule(start=stopped)
    #print(Display.schedule_to_string(schedule)) 

    register_shows(schedule, [shows["Penny Dreadful S3"]])
    del shows["Penny Dreadful S3"]
    stopped = schedule.generate_schedule(start=stopped)
    #print(Display.schedule_to_string(schedule)) 

    register_shows(schedule, [shows["Dickinson S1"], shows["Slow Horses S5"]])
    del shows["Dickinson S1"]
    del shows["Slow Horses S5"]
    stopped = schedule.generate_schedule(start=stopped)
    #print(Display.schedule_to_string(schedule)) 

    register_shows(schedule, [shows["Your Friends & Neighbors"], shows["Chief of War"]])
    del shows["Your Friends & Neighbors"]
    del shows["Chief of War"]
    stopped = schedule.generate_schedule(start=stopped, stop_at_first_empty_show=False, end=date(2025, 10, 13))
    #print(Display.schedule_to_string(schedule)) 

    register_shows(schedule, [shows["Gen V S2"], shows["The Talamasca"]])
    del shows["Gen V S2"]
    del shows["The Talamasca"]
    stopped = schedule.generate_schedule(start=stopped)
    stopped = schedule.generate_schedule(start=stopped)
    print(Display.schedule_to_string(schedule)) 

    print("=================Copy-Pastable CSV schedule:=================\n")
    print(Display.schedule_paste_format(schedule, shows.values()))

    spacer = 0