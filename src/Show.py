from __future__ import annotations
from typing import Callable, Optional, cast
from datetime import datetime, timedelta
from Episode import Episode, EpisodeBuilder
from sortedcontainers import SortedList

class Show:
    def __init__(
            self: Show,
            name: str,
            color: int = -1,
            episodes: Optional[SortedList] = None,
            priority: int = 0) -> None:
        self.name: str = name
        self.episodes: SortedList = episodes if episodes else SortedList(key=lambda ep: ep.episode_order)
        self.priority: int = priority
        self.color: int = color


class ShowBuilder:
    def __init__(self: ShowBuilder, name: str = "", show: Optional[Show] = None) -> None:
        self.show: Show
        if show:
            self.show = show
        else:
            self.show = Show(name)

    def WithPriority(self: ShowBuilder, priority: int) -> ShowBuilder:
        self.show.priority = priority
        return self

    def WithColor(self: ShowBuilder, color: int) -> ShowBuilder:
        self.show.color = color
        return self

    def WithEpisode(self: ShowBuilder, generator: Callable[[EpisodeBuilder]]) -> ShowBuilder:
        ep_builder: EpisodeBuilder = EpisodeBuilder(show_name=self.show.name)
        generator(ep_builder)
        self.show.episodes.add(ep_builder.episode)
        return self

    def WithEpisodes(self: ShowBuilder, num_episodes: int, start_episode: int = 1, available_on: Optional[datetime] = None) -> ShowBuilder:
        for i in range(start_episode, num_episodes + 1):
            self.WithEpisode(lambda ep_generator: ep_generator
                             .EpisodeNumber(i)
                             .AvailableAt(available_on))
        self.FinalizeLastEpisode()
        return self

    def WithWeeklyEpisodes(self: ShowBuilder, start_date: datetime, num_episodes: int, start_episode: int = 1) -> ShowBuilder:
        for i in range(start_episode, num_episodes + 1):
            week_num: int = i - start_episode
            self.WithEpisode(lambda ep_generator: ep_generator
                             .EpisodeNumber(i)
                             .AvailableAt(start_date + timedelta(days = week_num * 7)))
        self.FinalizeLastEpisode()
        return self

    def FinalizeLastEpisode(self: ShowBuilder) -> ShowBuilder:
        cast(Episode, self.show.episodes[-1]).make_last()
        return self