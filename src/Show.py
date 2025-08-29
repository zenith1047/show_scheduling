from __future__ import annotations
from typing import Callable, Optional, Tuple, Union
from datetime import datetime, timedelta
from Episode import Episode, EpisodeBuilder, LastEpisode, EpisodeKey
from SortedList import SortedList

class Show:
    def __init__(
            self: Show,
            name: str,
            episodes: Optional[SortedList[Episode]] = None,
            priority: int = 0) -> None:
        self.name: str = name
        self.episodes: SortedList[Episode] = episodes if episodes else SortedList[Episode](key_accessor=EpisodeKey)
        self.priority: int = priority


def ShowKey(item: Show) -> int:
    return item.priority


class ShowBuilder:
    def __init__(self: ShowBuilder, show: Optional[Show] = None):
        self.show: Union[Show, None] = show

    def CreateShow(self: ShowBuilder, name: str) -> ShowBuilder:
        self.show = Show(name)
        return self

    def WithPriority(self: ShowBuilder, priority: int) -> ShowBuilder:
        self.show.priority = priority
        return self

    def WithEpisode(self: ShowBuilder, generator: Callable[[EpisodeBuilder]]) -> ShowBuilder:
        ep_builder: EpisodeBuilder = EpisodeBuilder()
        generator(ep_builder)
        self.show.episodes.append(ep_builder.episode)
        return self

    def WithEpisodes(self: ShowBuilder, num_episodes: int, start_episode: Optional[int] = 1, available_on: Optional[datetime] = None) -> ShowBuilder:
        for i in range(start_episode, num_episodes + 1):
            self.WithEpisode(lambda ep_generator: ep_generator
                             .CreateEpisode(i, self.show.name)
                             .AvailableAt(available_on))
        self.FinalizeLastEpisode()
        return self

    def WithWeeklyEpisodes(self: ShowBuilder, start_date: datetime, num_episodes: int, start_episode: Optional[int] = 1) -> ShowBuilder:
        for i in range(start_episode, num_episodes + 1):
            week_num: int = i - start_episode
            self.WithEpisode(lambda ep_generator: ep_generator
                             .CreateEpisode(i, self.show.name)
                             .AvailableAt(start_date + timedelta(days = week_num * 7)))
        self.FinalizeLastEpisode()
        return self

    def FinalizeLastEpisode(self: ShowBuilder) -> ShowBuilder:
        self.show.episodes[-1] = LastEpisode.MakeLast(self.show.episodes[-1])
        return self