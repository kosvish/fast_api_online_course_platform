from pydantic import BaseModel


class TokenInfo(BaseModel):
    token: str
    type: str