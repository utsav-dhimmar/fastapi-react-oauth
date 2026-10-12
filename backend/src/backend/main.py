import logging
import sys

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware

from .auth import oauth
from .config import settings
from .schemas import GoogleAuthPayload, SayHi

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


@app.post("/auth/google")
async def auth_google(payload: GoogleAuthPayload, request: Request):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": payload.code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "postmessage",  # Required for Google Identity Services auth-code flow via popup
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)

    if token_response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Failed to obtain access token from Google",
        )
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Failed to obtain access token from Google",
        )

    async with httpx.AsyncClient() as client:
        userinfo_response = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if userinfo_response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Failed to obtain user info from Google",
        )
    userinfo = userinfo_response.json()
    request.session["user"] = userinfo
    return userinfo
