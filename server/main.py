"""Server for codenames game"""
import asyncio
import datetime
import enum
import functools
import typing
from typing import Annotated, Any
from uuid import UUID, uuid4

from fastapi import (BackgroundTasks, Depends, FastAPI, Header, HTTPException,
                     WebSocket, WebSocketDisconnect, WebSocketException,
                     status)
from pydantic import BaseModel, ConfigDict, Field, validator


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


class Participant(BaseModel):
    """Participant in a room"""

    role: RoomRole
    sockets: list[WebSocket] = Field(default_factory=list)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Room(BaseModel):
    """Room information"""

    words: list[str]
    colors: list[CellColor]
    revealed: list[bool] = Field(default_factory=lambda: [False] * 25)
    participants: dict[str, Participant] = Field(default_factory=dict)
    creation: datetime.datetime = Field(default_factory=datetime.datetime.now)


class RoomCreationParams(BaseModel):
    """Information needed to create a new room"""

    words: list[str]
    colors: list[CellColor]

    @validator("words")
    # pylint: disable=no-self-argument
    def words_long_enough(cls, wordlist: list[str]) -> list[str]:
        """Check that the word list provided is correct"""
        length_matches = len(wordlist) == 25
        wordlength_matches = all(len(x) < 25 for x in wordlist)
        if not length_matches:
            raise ValueError("Word list wrong size")
        if not wordlength_matches:
            raise ValueError("Words in word list too long")
        return wordlist

    @validator("colors")
    # pylint: disable=no-self-argument
    def colors_long_enough(cls, colorlist: list[CellColor]) -> list[CellColor]:
        """Check that the color list provided is correct"""
        if len(colorlist) != 25:
            raise ValueError("Color list wrong size")
        return colorlist


class RoomCreationResponse(BaseModel):
    """Response for room creation"""

    id: UUID
    token: str


ROOMS: dict[UUID, Room] = {}

app = FastAPI()


@app.post("/room", status_code=status.HTTP_201_CREATED)
def create_room(params: RoomCreationParams) -> RoomCreationResponse:
    """Create a new room"""
    if len(ROOMS) > 100:
        raise HTTPException(status_code=500, detail="Too many rooms")
    room_id = uuid4()
    if room_id in ROOMS:
        raise HTTPException(status_code=500, detail="Bad luck")
    admintoken = uuid4().hex
    ROOMS[room_id] = Room(
        words=params.words,
        colors=params.colors,
        participants={admintoken: Participant(role=RoomRole.ADMIN)},
    )
    return RoomCreationResponse(id=room_id, token=admintoken)


class RoomCredentials:
    """Authorize user from HTTP Request"""

    def __init__(self, room_id: UUID, authorization: Annotated[str, Header()]):
        room = ROOMS[room_id]
        token = authorization.replace("Bearer ", "")
        access_forbidden_exception = HTTPException(status_code=401)
        if token not in room.participants:
            raise access_forbidden_exception
        self.token = token
        self.room_id = room_id
        self.role = room.participants[token].role

    @property
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role == RoomRole.ADMIN


@app.patch("/room/{room_id}")
def change_room(
    room_id: UUID,
    params: RoomCreationParams,
    creds: Annotated[RoomCredentials, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    """Change room information"""
    if not creds.is_admin:
        raise HTTPException(status_code=401)
    room = ROOMS[room_id]
    room.words = params.words
    room.colors = params.colors
    room.revealed = [False] * 25
    background_tasks.add_task(notify_participants, room_id)


@app.delete("/room/{room_id}")
def delete_room(
    room_id: UUID,
    creds: Annotated[RoomCredentials, Depends()],
) -> None:
    """Delete room"""
    if not creds.is_admin:
        raise HTTPException(status_code=401)
    del ROOMS[room_id]


class RoomInfo(BaseModel):
    """Room information"""

    words: list[str]
    revealed: list[bool]
    colors: list[CellColor | None]


@app.get("/room/{room_id}")
def get_room(
    room_id: UUID,
    creds: Annotated[RoomCredentials, Depends()],
) -> RoomInfo:
    """Get room information"""
    room = ROOMS[room_id]
    if creds.role in [RoomRole.ADMIN, RoomRole.SPYMASTER]:
        return RoomInfo(
            words=room.words,
            revealed=room.revealed,
            colors=typing.cast(list[CellColor | None], room.colors),
        )
    return RoomInfo(
        words=room.words,
        revealed=room.revealed,
        colors=[
            color if cellOpen else None
            for color, cellOpen in zip(room.colors, room.revealed)
        ],
    )


async def notify_participants(room_id: UUID) -> None:
    """Notify participants of updates"""
    todo = (s for y in ROOMS[room_id].participants.values() for s in y.sockets)
    sendings = [t.send_bytes(b"G") for t in todo]
    await asyncio.gather(*sendings)


@app.put("/room/{room_id}/{cell}")
def click_room(
    room_id: UUID,
    cell: int,
    creds: Annotated[RoomCredentials, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    """Send click to room"""
    room = ROOMS[room_id]

    if creds.role == RoomRole.SPECTATOR:
        raise HTTPException(status_code=401)
    if not room.revealed[cell]:
        room.revealed[cell] = True
        background_tasks.add_task(notify_participants, room_id)


@app.get("/role/{room_id}")
def get_role(creds: Annotated[RoomCredentials, Depends()]) -> RoomRole:
    """Get role of user"""
    return creds.role


@app.post("/roomShare/{room_id}/{role}")
def make_share(
    room_id: UUID, creds: Annotated[RoomCredentials, Depends()], role: RoomRole
) -> str:
    """Create share code"""
    if creds.role < role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new_token = uuid4().hex
    ROOMS[room_id].participants[new_token] = Participant(role=role)
    return new_token


@app.websocket("/roomSubscription/{room_id}")
async def subscribe_room(websocket: WebSocket, room_id: UUID) -> None:
    """Open websocket for room updates"""
    await websocket.accept()
    room = ROOMS[room_id]
    token = await websocket.receive_text()
    if token not in room.participants:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized"
        )
    ROOMS[room_id].participants[token].sockets.append(websocket)
    try:
        while True:
            await websocket.receive_bytes()
    except WebSocketDisconnect:
        ROOMS[room_id].participants[token].sockets.remove(websocket)
