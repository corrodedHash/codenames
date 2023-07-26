"""Server for codenames game"""


from fastapi import FastAPI

from .routes.room import router as room_router
from .routes.other import router as other_router


app = FastAPI()
app.include_router(room_router)
app.include_router(other_router)
