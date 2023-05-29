from flask import Flask, request, make_response

import uuid
import time

app = Flask(__name__)


class Room:
    created: float
    words: list[str]
    colors: list[str]
    adminkey: str


rooms: dict[str, Room] = {}
MAX_ROOMS = 50000


def fix_cors(f):
    def x(*args, **kwargs):
        r = f(*args, **kwargs)
        response = make_response(r)

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return x


@app.route("/create/", methods=["POST"])
def create_rooms():
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
    newRoom.created = time.time()
    rooms[sessionkey.hex] = newRoom
    return {"sessionkey": sessionkey.hex, "adminkey": adminkey.hex}


@app.route("/list/")
@fix_cors
def list_rooms():
    return [{"sessionkey": k, "created": r.created} for (k, r) in rooms.items()]


@app.route("/get_user/<sessionkey>/")
def get_info(sessionkey: str):
    if sessionkey not in rooms:
        return ("Unknown sessionkey", 400)
    return {"words": rooms[sessionkey].words}


@app.route("/get_all/<sessionkey>/")
def get_all_info(sessionkey: str):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        return ("Not authenticated", 401)
    if sessionkey not in rooms:
        return ("Unknown sessionkey", 400)
    room = rooms[sessionkey]
    if room.adminkey != auth_token:
        return ("Unknown adminkey", 400)
    return {"words": room.words, "colors": room.colors}
