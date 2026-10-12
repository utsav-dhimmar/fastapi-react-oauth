from pydantic import BaseModel


class SayHi(BaseModel):
    message: str
