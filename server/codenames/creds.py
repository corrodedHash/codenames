"""FastAPI dependency to manage room affiliation and authority"""
from typing import Annotated
from uuid import UUID

from fastapi import Header, HTTPException, status

from .rooms import ROOMS
from .types import RoomRole


class RoomCredentials:
    """Authorize user from HTTP Request"""

    def __init__(self, room_id: UUID, authorization: Annotated[str, Header()]):
        try:
            room = ROOMS[room_id]
        except KeyError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room does not exist"
            ) from exc
        token = authorization.replace("Bearer ", "")
        access_forbidden_exception = HTTPException(status_code=401)
        found_participant = [x for x in room.participants if x.token == token]
        if not found_participant:
            raise access_forbidden_exception
        self.user = found_participant[0]
        self.room_id = room_id
        self.room = room

    @property
    def role(self) -> RoomRole:
        """Return role of user"""
        return self.user.role

    @property
    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.role == RoomRole.ADMIN
