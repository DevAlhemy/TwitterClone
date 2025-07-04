from fastapi.staticfiles import StaticFiles
from endpoints import users, medias, tweets
from fastapi import FastAPI
import os


app = FastAPI(title="Twitter", version="1.0.0")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tweets.router, prefix="/api/tweets", tags=["tweets"])
app.include_router(medias.router, prefix="/api/medias", tags=["medias"])

app.mount("/media", StaticFiles(directory=os.path.join(BASE_DIR, "app", "media")), name="media")
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static"), html=True), name="static")
