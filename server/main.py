"""Server for codenames game"""
import asyncio
import datetime
import enum
import functools
import json
import random
import typing
from typing import Annotated, Any, Callable, Self, TypeVar
from uuid import UUID, uuid4
import dataclasses
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
from pydantic import BaseModel, ConfigDict, validator

RANDOM_NAME_POOL = "ut_names.txt"


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

    async def broadcast(self, message: str):
        """Notify participants of updates"""
        todo = (s for y in self.participants for s in y.sockets)
        sendings = [t.send_text(message) for t in todo]
        await asyncio.gather(*sendings)

    async def broadcast_event(
        self,
        eventname: str,
        info: dict[str, Any],
        actor: str | None,
    ):
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


class UserSummary(BaseModel):
    """Non-sensitive user information"""

    user_id: str
    displayname: str
    online: bool
    role: RoomRole

    @classmethod
    def summarize(cls, participant: Participant) -> Self:
        """Create a `UserSummary` from `Participant` type"""
        return UserSummary(
            user_id=participant.identifier,
            displayname=participant.displayname,
            online=len(participant.sockets) > 0,
            role=participant.role,
        )


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
        participants=[
            Participant(
                token=admintoken,
                role=RoomRole.ADMIN,
                displayname="Adam",
            )
        ],
    )
    ROOMS[room_id].participants[0].displayname = ROOMS[room_id].displayname_pool.pop()
    return RoomCreationResponse(id=room_id, token=admintoken)


class RoomCredentials:
    """Authorize user from HTTP Request"""

    def __init__(self, room_id: UUID, authorization: Annotated[str, Header()]):
        room = ROOMS[room_id]
        token = authorization.replace("Bearer ", "")
        access_forbidden_exception = HTTPException(status_code=401)
        found_participant = [x for x in room.participants if x.token == token]
        if not found_participant:
            raise access_forbidden_exception
        self.user = found_participant[0]
        self.room_id = room_id

    @property
    def role(self) -> RoomRole:
        """Return role of user"""
        return self.user.role

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
    background_tasks.add_task(
        room.broadcast_event,
        eventname="roomchange",
        info={},
        actor=creds.user.identifier,
    )


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
        background_tasks.add_task(
            room.broadcast_event,
            eventname="click",
            info={"cell": cell},
            actor=creds.user.identifier,
        )


@app.get("/role/{room_id}")
def get_role(creds: Annotated[RoomCredentials, Depends()]) -> RoomRole:
    """Get role of user"""
    return creds.role


@app.get("/user/{room_id}")
def get_users(creds: Annotated[RoomCredentials, Depends()]) -> list[UserSummary]:
    """List all users in room"""
    return [UserSummary.summarize(p) for p in ROOMS[creds.room_id].participants]


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


@app.post("/roomShare/{room_id}/{role}")
def make_share(
    room_id: UUID, creds: Annotated[RoomCredentials, Depends()], role: RoomRole
) -> str:
    """Create share code"""
    if creds.role < role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new_token = try_n_times(
        lambda: uuid4().hex,
        lambda x: len([p for p in ROOMS[room_id].participants if p.token == x]) == 0,
        5,
    )
    new_identifier = try_n_times(
        lambda: uuid4().hex,
        lambda x: len([p for p in ROOMS[room_id].participants if p.identifier == x])
        == 0,
        5,
    )
    if new_token is None or new_identifier is None:
        raise RuntimeError("Could not generate token")
    ROOMS[room_id].participants.append(
        Participant(
            role=role,
            token=new_token,
            identifier=new_identifier,
            displayname=ROOMS[room_id].displayname_pool.pop(),
        )
    )
    return new_token


@app.websocket("/roomSubscription/{room_id}")
async def subscribe_room(websocket: WebSocket, room_id: UUID) -> None:
    """Open websocket for room updates"""
    await websocket.accept()
    room = ROOMS[room_id]
    token = await websocket.receive_text()
    user = [x for x in room.participants if x.token == token]
    if not user:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized"
        )
    if len(user[0].sockets) == 0:
        await room.broadcast_event(
            eventname="useronline", info={}, actor=user[0].identifier
        )
    user[0].sockets.append(websocket)
    try:
        while True:
            await websocket.receive_bytes()
    except WebSocketDisconnect:
        user[0].sockets.remove(websocket)
        if len(user[0].sockets) == 0:
            await room.broadcast_event(
                eventname="useroffline", info={}, actor=user[0].identifier
            )
