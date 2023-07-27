"""FastAPI routes for accessing a room"""
import base64
import typing
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, validator

from codenames.creds import RoomCredentials
from codenames.util import try_n_times

from ..rooms import ROOMS
from ..types import CellColor, Participant, Room, RoomRole

router = APIRouter()


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

    id: str
    token: str
    identifier: str
    displayname: str


@router.patch("/room/{room_id}")
def change_room(
    params: RoomCreationParams,
    creds: Annotated[RoomCredentials, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    """Change room information"""
    if not creds.is_admin:
        raise HTTPException(status_code=401)
    creds.room.words = params.words
    creds.room.colors = params.colors
    creds.room.revealed = [False] * 25
    background_tasks.add_task(
        creds.room.broadcast_event,
        eventname="roomchange",
        info={},
        actor=creds.user.identifier,
    )


@router.delete("/room/{room_id}")
def delete_room(
    creds: Annotated[RoomCredentials, Depends()],
) -> None:
    """Delete room"""
    if not creds.is_admin:
        raise HTTPException(status_code=401)
    del ROOMS[creds.room_id]


class RoomInfo(BaseModel):
    """Room information"""

    words: list[str]
    revealed: list[bool]
    colors: list[CellColor | None]


@router.get("/room/{room_id}")
def get_room(
    creds: Annotated[RoomCredentials, Depends()],
) -> RoomInfo:
    """Get room information"""
    room = creds.room
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


@router.post("/room", status_code=status.HTTP_201_CREATED)
def create_room(params: RoomCreationParams) -> RoomCreationResponse:
    """Create a new room"""
    if len(ROOMS) > 100:
        raise HTTPException(status_code=500, detail="Too many rooms")
    room_id = try_n_times(
        lambda: base64.b64encode(uuid4().bytes[:9], b"-_").decode("utf-8"),
        lambda x: x not in ROOMS,
        5,
    )

    if room_id is None:
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
    admin = ROOMS[room_id].participants[0]
    admin.displayname = ROOMS[room_id].displayname_pool.pop()
    return RoomCreationResponse(
        id=room_id,
        token=admintoken,
        identifier=admin.identifier,
        displayname=admin.displayname,
    )
