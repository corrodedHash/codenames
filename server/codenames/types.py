"""Types for codenames"""

import asyncio
import datetime
import enum
import functools
import json
from typing import Any
from uuid import uuid4
import dataclasses
from fastapi import WebSocket
from pydantic import ConfigDict

from codenames.naming import shuffle_random_pool


class CellColor(str, enum.Enum):
    """Possible states of a cell"""

    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    NEUTRAL = "neutral"


@functools.total_ordering
class RoomRole(str, enum.Enum):
    """Possible roles of user in room"""

    ADMIN = "admin"
    SPYMASTER = "spymaster"
    REVEALER = "revealer"
    SPECTATOR = "spectator"

    def __lt__(self, other: Any) -> bool:
        value_map = {"admin": 0, "spymaster": 1, "revealer": 2, "spectator": 3}
        return value_map[self] > value_map[other]


@dataclasses.dataclass
class Participant:
    """Participant in a room"""

    role: RoomRole
    displayname: str
    token: str = dataclasses.field(default_factory=lambda: uuid4().hex)
    identifier: str = dataclasses.field(default_factory=lambda: uuid4().hex)
    sockets: list[WebSocket] = dataclasses.field(default_factory=list)
    model_config = ConfigDict(arbitrary_types_allowed=True)


@dataclasses.dataclass
class Room:
    """Room information"""

    words: list[str]
    colors: list[CellColor]
    revealed: list[bool] = dataclasses.field(default_factory=lambda: [False] * 25)
    participants: list[Participant] = dataclasses.field(default_factory=list)
    displayname_pool: list[str] = dataclasses.field(default_factory=shuffle_random_pool)
    creation: datetime.datetime = dataclasses.field(
        default_factory=datetime.datetime.now
    )

    async def broadcast(self, message: str) -> None:
        """Notify participants of updates"""
        todo = (s for y in self.participants for s in y.sockets)
        sendings = [t.send_text(message) for t in todo]
        await asyncio.gather(*sendings)

    async def broadcast_event(
        self,
        eventname: str,
        info: dict[str, Any],
        actor: str | None,
    ) -> None:
        """Notify participants of event"""
        actor_instance = [x for x in self.participants if x.identifier == actor]
        actordict = (
            {
                "user": actor,
                "displayname": actor_instance[0].displayname
                if actor_instance[0]
                else None,
            }
            if actor
            else {}
        )
        await self.broadcast(json.dumps({"event": eventname} | actordict | info))
