import asyncio
import datetime
import enum
import functools
import typing
from typing import Annotated, Self
from uuid import UUID, uuid4

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from pydantic import BaseModel, Field, validator


class CellColor(str, enum.Enum):
    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    NEUTRAL = "neutral"


@functools.total_ordering
class RoomRole(str, enum.Enum):
    ADMIN = "admin"
    SPYMASTER = "spymaster"
    REVEALER = "revealer"
    SPECTATOR = "spectator"

    def __lt__(self, other: Self):
        value_map = {"admin": 0, "spymaster": 1, "revealer": 2, "spectator": 3}
        return value_map[self] > value_map[other]


class Participant(BaseModel):
    role: RoomRole
    sockets: list[WebSocket] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class Room(BaseModel):
    words: list[str]
    colors: list[CellColor]
    revealed: list[bool] = Field(default_factory=lambda: [False] * 25)
    clickState: int = 0
    roomState: int = 0
    participantTokens: dict[str, Participant] = Field(default_factory=dict)
    creation: datetime.datetime = Field(default_factory=datetime.datetime.now)


class RoomCreationParams(BaseModel):
    words: list[str]
    colors: list[CellColor]

    @validator("words")
    def words_long_enough(cls, v: list[str]) -> list[str]:
        length_matches = len(v) == 25
        wordlength_matches = all(len(x) < 25 for x in v)
        if not length_matches:
            raise ValueError("Word list wrong size")
        if not wordlength_matches:
            raise ValueError("Words in word list too long")
        return v

    @validator("colors")
    def colors_long_enough(cls, v: list[CellColor]) -> list[CellColor]:
        if len(v) != 25:
            raise ValueError("Color list wrong size")
        return v


class RoomUpdateStatus(BaseModel):
    clickState: int
    roomState: int


class RoomSummary(BaseModel):
    id: UUID
    name: str


class RoomCreationResponse(BaseModel):
    id: UUID
    token: str


ROOMS: dict[UUID, Room] = {}

app = FastAPI()


@app.get("/rooms")
def list_rooms() -> list[RoomSummary]:
    return [
        RoomSummary(id=k, name="".join([x.replace(" ", "") for x in v.words[:3]]))
        for k, v in ROOMS.items()
    ]


@app.post("/room", status_code=status.HTTP_201_CREATED)
def create_room(params: RoomCreationParams) -> RoomCreationResponse:
    if len(ROOMS) > 100:
        raise HTTPException(status_code=500, detail="Too many rooms")
    roomID = uuid4()
    if roomID in ROOMS:
        raise HTTPException(status_code=500, detail="Bad luck")
    admintoken = uuid4().hex
    ROOMS[roomID] = Room(
        words=params.words,
        colors=params.colors,
        participantTokens={admintoken: Participant(role=RoomRole.ADMIN)},
    )
    return RoomCreationResponse(id=roomID, token=admintoken)


class RoomCredentials:
    def __init__(self, roomID: UUID, authorization: Annotated[str, Header()]):
        room = ROOMS[roomID]
        token = authorization.replace("Bearer ", "")
        access_forbidden_exception = HTTPException(status_code=401)
        if token not in room.participantTokens:
            raise access_forbidden_exception
        self.token = token
        self.roomID = roomID
        self.role = room.participantTokens[token].role

    @property
    def isAdmin(self) -> bool:
        return self.role == RoomRole.ADMIN


@app.patch("/room/{roomID}")
def change_room(
    roomID: UUID,
    params: RoomCreationParams,
    creds: Annotated[RoomCredentials, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    if not creds.isAdmin:
        raise HTTPException(status_code=401)
    room = ROOMS[roomID]
    room.words = params.words
    room.colors = params.colors
    room.revealed = [False] * 25
    room.roomState += 1
    background_tasks.add_task(notify_participants, roomID)


@app.delete("/room/{roomID}")
def delete_room(
    roomID: UUID,
    creds: Annotated[RoomCredentials, Depends()],
) -> None:
    if not creds.isAdmin:
        raise HTTPException(status_code=401)
    del ROOMS[roomID]


class RoomInfo(BaseModel):
    words: list[str]
    revealed: list[bool]
    colors: list[CellColor | None]


@app.get("/room/{roomID}")
def get_room(
    roomID: UUID,
    creds: Annotated[RoomCredentials, Depends()],
) -> RoomInfo:
    room = ROOMS[roomID]
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


async def notify_participants(roomID: UUID):
    todo = (s for y in ROOMS[roomID].participantTokens.values() for s in y.sockets)
    sendings = [t.send_bytes(b"G") for t in todo]
    await asyncio.gather(*sendings)


@app.put("/room/{roomID}/{cell}")
def click_room(
    roomID: UUID,
    cell: int,
    creds: Annotated[RoomCredentials, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    room = ROOMS[roomID]

    if creds.role == RoomRole.SPECTATOR:
        raise HTTPException(status_code=401)
    if not room.revealed[cell]:
        room.clickState += 1
        room.revealed[cell] = True
        background_tasks.add_task(notify_participants, roomID)


@app.get("/role/{roomID}")
def get_role(creds: Annotated[RoomCredentials, Depends()]) -> RoomRole:
    return creds.role


@app.post("/roomShare/{roomID}/{role}")
def make_share(
    roomID: UUID, creds: Annotated[RoomCredentials, Depends()], role: RoomRole
) -> str:
    if creds.role < role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new_token = uuid4().hex
    ROOMS[roomID].participantTokens[new_token] = Participant(role=role)
    return new_token


@app.websocket("/roomSubscription/{roomID}")
async def subscribe_room(websocket: WebSocket, roomID: UUID):
    print("hi" + roomID.hex)
    await websocket.accept()
    room = ROOMS[roomID]
    token = await websocket.receive_text()
    if token not in room.participantTokens:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized"
        )
    ROOMS[roomID].participantTokens[token].sockets.append(websocket)
    try:
        while True:
            await websocket.receive_bytes()
    except WebSocketDisconnect:
        ROOMS[roomID].participantTokens[token].sockets.remove(websocket)


@app.get("/roomUpdates/{roomID}")
def get_room_updates(
    roomID: UUID,
    _creds: Annotated[RoomCredentials, Depends()],
) -> RoomUpdateStatus:
    room = ROOMS[roomID]
    return RoomUpdateStatus(clickState=room.clickState, roomState=room.roomState)
