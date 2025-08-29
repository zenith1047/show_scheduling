from __future__ import annotations
from typing import Callable, List, Optional, Union
from datetime import datetime

class Episode:
    def __init__(
            self: Episode,
            show_name: str,
            label: str,
            order: int = -1,
            release_date: Optional[datetime] = None,
            filters: Optional[List[Callable[[Episode, datetime], bool]]] = None) -> None:
        self.show_name: str = show_name
        self.episode_label: str = label
        self.episode_order: int = int(label) if label.isdigit() else order
        self.release_date: Optional[datetime] = release_date
        self.availability_filters: List[Callable[[Episode, datetime], bool]] = filters if filters else [lambda ep, slot: True]

    def display_name(self: Episode) -> str:
        display: str = f"{self.show_name} {self.episode_label}"
        if self.release_date:
            display += f" {self.release_date.strftime("[%b %d]")}"
        return display

    def is_available(self: Episode, slot: datetime) -> bool:
        for filter in self.availability_filters:
            if not filter(self, slot):
                return False
        return True

    def make_last(self: Episode):
        self.episode_label = f"({self.episode_label})"


class NonEpisode(Episode):
    def __init__(
            self:NonEpisode,
            show_name: str) -> None:
        super().__init__(show_name, "-1")


class EpisodeBuilder:
    def __init__(self: EpisodeBuilder, show_name: str = "", label: str = "-1", episode: Optional[Episode] = None):
        self.episode: Episode
        if episode:
            self.episode = episode
        else:
            self.episode = Episode(show_name, label)

    def EpisodeLabel(self: EpisodeBuilder, episode: str, order: int) -> EpisodeBuilder:
        self.episode.episode_label = episode
        self.episode.episode_order = order
        return self

    def EpisodeNumber(self: EpisodeBuilder, episode: int) -> EpisodeBuilder:
        self.episode.episode_order = episode
        self.episode.episode_label = str(episode)
        return self
    
    def AvailableAt(self: EpisodeBuilder, release: Union[datetime, None]) -> EpisodeBuilder:
        if release:
            self.episode.release_date = release
            self.episode.availability_filters.append(lambda ep, slot: ep.release_date <= slot if ep.release_date else True)
        return self
    
    def OnFridays(self: EpisodeBuilder) -> EpisodeBuilder:
        self.episode.availability_filters.append(lambda _, slot: slot.weekday() == 4)
        return self

    def OnSaturdays(self: EpisodeBuilder) -> EpisodeBuilder:
        self.episode.availability_filters.append(lambda _, slot: slot.weekday() == 5)
        return self