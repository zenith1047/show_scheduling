from typing import Iterable, Callable
from datetime import date, datetime
from Schedule import Schedule, ScheduleBuilder
from Show import Show, ShowBuilder
import Display


def add_show_to_pool(pool: dict[str, Show], name: str, config: Callable[[ShowBuilder], ShowBuilder]) -> None:
    builder: ShowBuilder = ShowBuilder(name=name)
    config(builder)
    builder.WithPriority(len(pool) + 1)
    if builder.show:
        pool[name] = builder.show


def build_show_pool() -> dict[str, Show]:
    pool: dict[str, Show] = {}
    add_show_to_pool(pool, "Peacemaker S2", lambda builder: builder
                     .WithColor(9)
                     .WithWeeklyEpisodes(datetime(2025, 8, 28, 21), num_episodes=8, start_episode=2))
    add_show_to_pool(pool, "Murderbot", lambda builder: builder
                     .WithColor(7)
                     .WithEpisode(lambda ep: ep.EpisodeLabel("2", 2))
                     .WithEpisode(lambda ep: ep.EpisodeLabel("3+4", 3)) 
                     .WithEpisode(lambda ep: ep.EpisodeLabel("5+6", 4))
                     .WithEpisode(lambda ep: ep.EpisodeLabel("7+8", 5))
                     .WithEpisode(lambda ep: ep.EpisodeLabel("9+10", 6))
                     .FinalizeLastEpisode())
    add_show_to_pool(pool, "Foundation S3", lambda builder: builder
                     .WithColor(5)
                     .WithEpisodes(num_episodes=10, start_episode=2))
    add_show_to_pool(pool, "Penny Dreadful S2", lambda builder: builder
                     .WithColor(10)
                     .WithEpisodes(num_episodes=10, start_episode=9))
    add_show_to_pool(pool, "Buccaneers S2", lambda builder: builder
                     .WithColor(1)
                     .WithEpisodes(num_episodes=8, start_episode=3))
    add_show_to_pool(pool, "Penny Dreadful S3", lambda builder: builder
                     .WithColor(11)
                     .WithEpisodes(num_episodes=9))
    add_show_to_pool(pool, "Slow Horses S5", lambda builder: builder
                     .WithColor(12)
                     .WithWeeklyEpisodes(start_date=datetime(2025, 9, 24), num_episodes=6))
    add_show_to_pool(pool, "Dickinson S1", lambda builder: builder
                     .WithColor(4)
                     .WithEpisodes(num_episodes=10))
    add_show_to_pool(pool, "Your Friends & Neighbors", lambda builder: builder
                     .WithColor(15)
                     .WithEpisodes(num_episodes=9))
    add_show_to_pool(pool, "Chief of War", lambda builder: builder
                     .WithColor(2)
                     .WithEpisodes(num_episodes=9))
    add_show_to_pool(pool, "Drops of God", lambda builder: builder
                     .WithColor(8)
                     .WithEpisodes(num_episodes=8))
    add_show_to_pool(pool, "Gen V S2", lambda builder: builder
                     .WithColor(6)
                     .WithEpisode(lambda ep: ep.EpisodeNumber(1).AvailableAt(datetime(2025, 9, 17)))
                     .WithEpisode(lambda ep: ep.EpisodeNumber(2).AvailableAt(datetime(2025, 9, 17)))
                     .WithEpisode(lambda ep: ep.EpisodeNumber(3).AvailableAt(datetime(2025, 9, 17)))
                     .WithWeeklyEpisodes(start_date=datetime(2025, 9, 24), num_episodes=8, start_episode=4))
    add_show_to_pool(pool, "The Talamasca", lambda builder: builder
                     .WithColor(14)
                     .WithWeeklyEpisodes(start_date=datetime(2025, 10, 26, 21), num_episodes=6))
    add_show_to_pool(pool, "Downton Abbey S1", lambda builder: builder
                     .WithColor(13)
                     .WithEpisodes(num_episodes=7))
    add_show_to_pool(pool, "Alien: Earth", lambda builder: builder
                     .WithColor(3)
                     .WithEpisodes(num_episodes=8))
    add_show_to_pool(pool, "Only Murders in the Building S5", lambda builder: builder
                     .WithEpisodes(num_episodes=10))
    return pool


def build_schedule_dates() -> Schedule:
    builder: ScheduleBuilder = ScheduleBuilder()

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


def register_shows(schedule: Schedule, shows: dict[str, Show], show_names: Iterable[str]) -> None:
    builder: ScheduleBuilder = ScheduleBuilder(schedule)
    for show_name in show_names:
        builder.RegisterShow(shows[show_name])
        del shows[show_name]


if __name__ == '__main__':
    #make this into a jupyter notebook for ease of on-the-fly script modification more like interactive workflow
    schedule: Schedule = build_schedule_dates()
    shows: dict[str, Show] = build_show_pool()

    start_date: date = date(2025, 8, 29)
    register_shows(schedule, shows, ["Peacemaker S2", "Murderbot", "Foundation S3", "Penny Dreadful S2", "Buccaneers S2"])
    stopped: date = schedule.generate_schedule(start=start_date)
    register_shows(schedule, shows, ["Penny Dreadful S3"])
    stopped = schedule.generate_schedule(start=stopped)
    register_shows(schedule, shows, ["Dickinson S1", "Slow Horses S5", "Your Friends & Neighbors"])
    stopped = schedule.generate_schedule(start=stopped)
    stopped = schedule.generate_schedule(start=stopped)
    register_shows(schedule, shows, ["Chief of War", "The Talamasca", "Drops of God"])
    stopped = schedule.generate_schedule(start=stopped)
    stopped = schedule.generate_schedule(start=stopped)
    stopped = schedule.generate_schedule(start=stopped)
    register_shows(schedule, shows, ["Gen V S2", "Downton Abbey S1", "Alien: Earth", "Only Murders in the Building S5"])
    stopped = schedule.generate_schedule(start=stopped, end=date(2025, 11, 1))

    print(Display.schedule_to_string(schedule)) 

    print("=================Copy-Pastable CSV schedule:=================\n")
    print(Display.schedule_paste_format(schedule, shows.values()))

    spacer = 0