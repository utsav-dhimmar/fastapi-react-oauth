from pydantic import BaseModel


class SayHi(BaseModel):
    message: str


class GoogleAuthPayload(BaseModel):
    code: str
