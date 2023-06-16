import enum
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator


class Room(BaseModel):
    words: list[str]
    colors: list[str]
    revealed: list[bool]
    clickState: int
    roomState: int
    adminTokens: list[str]
    participantTokens: list[str]


class CellColor(str, enum.Enum):
    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    NEUTRAL = "neutral"


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


ROOMS: dict[UUID, Room] = {}

app = FastAPI()


@app.get("/rooms")
def list_rooms():
    pass


@app.post("/room")
def create_room(params: RoomCreationParams):
    if len(ROOMS) > 100:
        raise HTTPException(status_code=507, detail="Too many rooms")
    token = uuid4()
    if token in ROOMS:
        raise HTTPException(status_code=500, detail="Bad luck")


@app.patch("/room/{roomID}")
def change_room(roomID: UUID, params: RoomCreationParams):
    pass


@app.get("/room/{roomID}")
def get_room(roomID: UUID):
    pass


@app.get("/roomUpdates/{roomID}")
def get_room_updates(roomID: UUID) -> RoomUpdateStatus:
    return RoomUpdateStatus(clickState=0, roomState=0)