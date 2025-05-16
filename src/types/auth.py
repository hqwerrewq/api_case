from typing import TypedDict, Literal


class TokenResponse(TypedDict):
    access_token: str
    token_type: Literal["bearer"]
