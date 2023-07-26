"""Unsorted routes"""
from typing import Annotated, Callable, TypeVar
from uuid import UUID, uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)

from ..creds import RoomCredentials
from ..rooms import ROOMS
from ..types import Participant, RoomRole

router = APIRouter()


@router.put("/room/{room_id}/{cell}")
def click_room(
    cell: int,
    creds: Annotated[RoomCredentials, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    """Send click to room"""
    room = creds.room

    if creds.role == RoomRole.SPECTATOR:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not room.revealed[cell]:
        room.revealed[cell] = True
        background_tasks.add_task(
            room.broadcast_event,
            eventname="click",
            info={"cell": cell},
            actor=creds.user.identifier,
        )


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


@router.post("/roomShare/{room_id}/{role}")
def make_share(creds: Annotated[RoomCredentials, Depends()], role: RoomRole) -> str:
    """Create share code"""
    if creds.role < role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new_token = try_n_times(
        lambda: uuid4().hex,
        lambda x: len([p for p in creds.room.participants if p.token == x]) == 0,
        5,
    )
    new_identifier = try_n_times(
        lambda: uuid4().hex,
        lambda x: len([p for p in creds.room.participants if p.identifier == x]) == 0,
        5,
    )
    if new_token is None or new_identifier is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not generate token",
            headers={"Retry-After": "0"},
        )
    creds.room.participants.append(
        Participant(
            role=role,
            token=new_token,
            identifier=new_identifier,
            displayname=creds.room.displayname_pool.pop(),
        )
    )
    return new_token


@router.websocket("/roomSubscription/{room_id}")
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
