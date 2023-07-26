"""Contains storage for room"""

from uuid import UUID

from .types import Room


ROOMS: dict[UUID, Room] = {}
