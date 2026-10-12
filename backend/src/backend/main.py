import logging
import sys

from fastapi import FastAPI
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware

from .auth import oauth
from .config import settings
from .schemas import SayHi

log = logging.getLogger("authlib")
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)


app = FastAPI()
app.add_middleware(
    middleware_class=SessionMiddleware, secret_key=settings.SECRET_KEY
)


@app.get("/", response_model=SayHi)
async def index():
    return {"message": "Hello World"}


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
    return user
