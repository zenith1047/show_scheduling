from __future__ import annotations
from typing import Callable, List, Optional, Union
from datetime import datetime

class Episode:
    def __init__(
            self: Episode,
            show_name: str,
            num: int,
            release_date: Optional[datetime] = None,
            filters: Optional[List[Callable[[Episode, datetime], bool]]] = None) -> None:
        self.show_name: str = show_name
        self.episode_number: int = num
        self.release_date: Optional[datetime] = release_date
        self.availability_filters: List[Callable[[Episode, datetime], bool]] = filters if filters else [lambda ep, slot: True]

    def display_name(self: Episode) -> str:
        display: str = f"{self.show_name} {self.episode_number}"
        display = self.append_date(display)
        return display

    def is_available(self: Episode, slot: datetime) -> bool:
        for filter in self.availability_filters:
            if not filter(self, slot):
                return False
        return True

    def append_date(self: Episode, display_name: str) -> str:
        if self.release_date:
            display_name += f" {self.release_date.strftime("[%b %d]")}"
        return display_name


class LastEpisode(Episode):
    def __init__(
            self: LastEpisode,
            show_name: str,
            num: int,
            release_date: Optional[datetime] = None,
            filters: Optional[List[Callable[[Episode, datetime], bool]]] = None) -> None:
        super().__init__(show_name, num, release_date, filters)

    def display_name(self: Episode) -> str:
        display: str = f"{self.show_name} ({self.episode_number})"
        display = self.append_date(display)
        return display

    def MakeLast(ep: Episode) -> LastEpisode:
        return LastEpisode(ep.show_name, ep.episode_number, ep.release_date, ep.availability_filters)


class NonEpisode(Episode):
    def __init__(
            self:NonEpisode,
            show_name: str) -> None:
        super().__init__(show_name, -1)


def EpisodeKey(ep: Episode) -> int:
    return ep.episode_number


class EpisodeBuilder:
    def __init__(self: EpisodeBuilder, episode: Optional[Episode] = None):
        self.episode: Union[Episode, None] = episode

    def CreateEpisode(self: EpisodeBuilder, episode: int, show_name: str) -> EpisodeBuilder:
        self.episode = Episode(show_name, episode)
        return self
    
    def AvailableAt(self: EpisodeBuilder, release: Union[datetime, None]) -> EpisodeBuilder:
        if release:
            self.episode.release_date = release
            self.episode.availability_filters.append(lambda ep, slot: ep.release_date <= slot)
        return self
    
    def OnFridays(self: EpisodeBuilder) -> EpisodeBuilder:
        self.episode.availability_filters.append(lambda _, slot: slot.weekday() == 4)
        return self

    def OnSaturdays(self: EpisodeBuilder) -> EpisodeBuilder:
        self.episode.availability_filters.append(lambda _, slot: slot.weekday() == 5)
        return self