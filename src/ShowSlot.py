from __future__ import annotations
from typing import Optional
from datetime import datetime
from Episode import Episode

class ShowSlot:
    def __init__(
            self: ShowSlot,
            time: datetime,
            episode: Optional[Episode] = None) -> None:
        self.time: datetime = time
        self.episode: Optional[Episode] = episode
