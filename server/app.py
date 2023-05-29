from flask import Flask, request, make_response

import uuid
import functools
import time

app = Flask(__name__)


class Room:
    created: float
    words: list[str]
    colors: list[str]
    revealed: list[bool]
    adminkey: str

    def revealedAsBitmap(self) -> int:
        masks = [1 << index for (index, r) in enumerate(self.revealed) if r]
        return functools.reduce(lambda x, y: x | y, masks, 0)


rooms: dict[str, Room] = {}
MAX_ROOMS = 50000


def fix_cors(f):
    @functools.wraps(f)
    def x(*args, **kwargs):
        r = f(*args, **kwargs)
        response = make_response(r)

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return x


@app.route("/create/", methods=["POST"])
def create_room():
    if len(rooms) > MAX_ROOMS:
        return ("Too many rooms", 500)
    sessionkey = uuid.uuid4()
    adminkey = uuid.uuid4()
    if sessionkey.hex in rooms:
        return ("Session key already exists, bad luck", 500)
    newRoom = Room()
    newRoom.adminkey = adminkey.hex
    newRoom.words = ["a", "b"]
    newRoom.colors = ["red", "blue"]
    newRoom.revealed = [False] * len(newRoom.words)
    newRoom.created = time.time()
    rooms[sessionkey.hex] = newRoom
    return {"sessionkey": sessionkey.hex, "adminkey": adminkey.hex}


@app.route("/list/")
@fix_cors
def list_rooms() -> list[dict[str, str | float]]:
    return [{"sessionkey": k, "created": r.created} for (k, r) in rooms.items()]


@app.route("/reveal/<sessionkey>/", method=["POST"])
def reveal_cell(sessionkey: str):
    if sessionkey not in rooms:
        return ("Unknown sessionkey", 400)
    room = rooms[sessionkey]
    if request.json is None:
        return ("Could not parse JSON", 400)
    try:
        cellIndex = int(request.json)
    except ValueError:
        return ("Could not read int from JSON", 400)
    if len(room.revealed) <= cellIndex:
        return ("Cellindex out of range", 400)
    room.revealed[cellIndex] = True
    return ("", 200)


@app.route("/get_user/<sessionkey>/")
def get_info(sessionkey: str) -> tuple[str, int] | dict[str, list[str] | int]:
    if sessionkey not in rooms:
        return ("Unknown sessionkey", 400)
    room = rooms[sessionkey]
    return {"words": room.words, "revealed": room.revealedAsBitmap()}


@app.route("/get_all/<sessionkey>/")
def get_all_info(sessionkey: str):
    auth_header = request.authorization
    if auth_header is not None and auth_header.token is not None:
        auth_token = auth_header.token
    else:
        return ("Not authenticated", 401)
    if sessionkey not in rooms:
        return ("Unknown sessionkey", 400)
    room = rooms[sessionkey]
    if room.adminkey != auth_token:
        return ("Unknown adminkey", 400)
    return {"words": room.words, "colors": room.colors}
