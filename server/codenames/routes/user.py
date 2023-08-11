"""Unsorted routes"""
import asyncio
from typing import Annotated, Self

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    WebSocket,
    status,
)
from pydantic import BaseModel

from ..creds import RoomCredentials
from ..types import Participant, RoomRole

router = APIRouter()


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


async def drop_user_sockets(sockets: list[WebSocket]) -> None:
    await asyncio.gather(*[x.close() for x in sockets])


@router.delete("/user/{room_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    creds: Annotated[RoomCredentials, Depends()],
    user_id: str,
    background_task: BackgroundTasks,
) -> None:
    if not creds.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    drop_user = [
        (index, x)
        for index, x in enumerate(creds.room.participants)
        if x.identifier == user_id
    ]
    if len(drop_user) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    (drop_index, drop_p) = drop_user[0]
    creds.room.participants.pop(drop_index)
    background_task.add_task(drop_user_sockets, drop_p.sockets)


@router.patch("/user/{room_id}/{user_id}/role/{role}")
def change_user_role(
    creds: Annotated[RoomCredentials, Depends()], user_id: str, role: RoomRole
) -> None:
    if not creds.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    drop_user = [x for x in creds.room.participants if x.identifier == user_id]
    if len(drop_user) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    (_, drop_p) = drop_user
    drop_p.role = role


@router.get("/user/{room_id}")
def get_users(creds: Annotated[RoomCredentials, Depends()]) -> list[UserSummary]:
    """List all users in room"""
    return [UserSummary.summarize(p) for p in creds.room.participants]


@router.get("/user/{room_id}/me")
def get_own_user(creds: Annotated[RoomCredentials, Depends()]) -> UserSummary:
    """Return own user info"""
    return UserSummary.summarize(creds.user)
