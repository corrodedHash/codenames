"""Utilities for generating displaynames"""
import functools
import random


RANDOM_NAME_POOL = "../ut_names.txt"


@functools.cache
def get_random_name_pool() -> list[str]:
    """Loads pool of random names, cached"""
    with open("ut_names.txt", "r", encoding="utf-8") as pool_file:
        return [x.strip() for x in pool_file.readlines()]


def get_random_name() -> str:
    """Chooses a random name"""
    return random.choice(get_random_name_pool())


def shuffle_random_pool() -> list[str]:
    """Shuffle random pool so that it is different for every room"""
    new_pool = get_random_name_pool()
    random.shuffle(new_pool)
    return new_pool
