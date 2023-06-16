import enum
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Header, status
from pydantic import BaseModel, validator, Field
import datetime


class CellColor(str, enum.Enum):
    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    NEUTRAL = "neutral"


class Room(BaseModel):
    words: list[str]
    colors: list[CellColor]
    revealed: list[bool] = Field(default_factory=lambda: [False] * 25)
    clickState: int = 0
    roomState: int = 0
    adminTokens: list[str] = Field(default_factory=list)
    participantTokens: list[str] = Field(default_factory=list)
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
        words=params.words, colors=params.colors, adminTokens=[admintoken]
    )
    return RoomCreationResponse(id=roomID, token=admintoken)


class RoomCredentials:
    def __init__(self, roomID: UUID, authorization: Annotated[str, Header()]):
        room = ROOMS[roomID]
        token = authorization.replace("Bearer ", "")
        self.isAdmin = token in room.adminTokens
        if not (self.isAdmin and token in room.participantTokens):
            raise HTTPException(status_code=401)


@app.patch("/room/{roomID}")
def change_room(
    roomID: UUID,
    params: RoomCreationParams,
    creds: Annotated[RoomCredentials, Depends()],
) -> None:
    if not creds.isAdmin:
        raise HTTPException(status_code=401)
    room = ROOMS[roomID]
    room.words = params.words
    room.colors = params.colors
    room.roomState += 1


@app.delete("/room/{roomID}")
def delete_room(
    roomID: UUID,
    creds: Annotated[RoomCredentials, Depends()],
) -> None:
    if not creds.isAdmin:
        raise HTTPException(status_code=401)
    del ROOMS[roomID]


@app.get("/room/{roomID}")
def get_room(roomID: UUID):
    pass


@app.get("/roomUpdates/{roomID}")
def get_room_updates(roomID: UUID) -> RoomUpdateStatus:
    return RoomUpdateStatus(clickState=0, roomState=0)
