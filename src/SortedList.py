from __future__ import annotations
from typing import Any, Union, Callable
from bisect import insort

#lower priority value is earlier in the list
#this does not allow for changing priority of an item in situ causing a reorder
class SortedList(list[Any]):
    def __init__(self: SortedList, key_accessor: Callable[[Any], Any]) -> None:
        self.key_accessor = key_accessor

    def append(self: SortedList, item: Any) -> None:
        insort(self, item, key= self.key_accessor)

    # to re-sort the list, in case priority of contents are changed
    def re_sort(self: SortedList) -> None:
        self.sort(key=self.key_accessor)
