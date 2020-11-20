from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from api.utils import Str, Int16
from app.response_models import ListModel, StatusModel

class ShortUserResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    email: Str
    firstname: Str
    age: Int16
    gender: Str
    height: Int16()
    is_smoke: bool
    hobbies: Str
    created_at: datetime

    class Config:
        orm_mode = True


class EnvelopedListOfUsersResponse(ListModel):
    data: List[UserResponse]


class EnvelopedUserResponse(StatusModel):
    data: UserResponse


class UserCreateRequest(BaseModel):
    email: Str
    password: Str
    firstname: Str
    lastname: Str
    age: Int16
    gender: Str
    height: int
    is_smoke: bool
    hobbies: Str


class UserUpdateRequest(BaseModel):
    email: Optional[Str]
    password: Optional[Str]
    firstname: Optional[Str]
    lastname: Optional[Str]
    age: Optional[Int16]
    gender: Optional[Str]
    height: Optional[int]
    is_smoke: Optional[bool]
    hobbies: Optional[Str]
