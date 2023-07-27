"""Utility functions"""
from typing import Callable, TypeVar


T = TypeVar("T")


def try_n_times(
    func: Callable[[], T], cond: Callable[[T], bool], n_times: int
) -> T | None:
    """Try to call a function n times, return None if cond returns false every time"""
    for _ in range(n_times):
        result = func()
        if cond(result):
            return result
    return None
