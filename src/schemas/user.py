import re
from typing import Optional

from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('email')
    def validate_email(cls, v):
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex, v):
            raise ValueError("Invalid email format")
        return v.lower()

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

class UserInDB(UserBase):
    id: int
    is_active: bool


class UserLogin(UserBase):
    password: str = Field(..., min_length=8)