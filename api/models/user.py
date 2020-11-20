from datetime import datetime
from typing import List

from pydantic import BaseModel

from api.utils import Str, Int16
from app.response_models import ListModel, StatusModel


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


class EnvelopedListOfUsersResponse(ListModel):
    data: List[UserResponse]


class EnvelopedUserResponse(StatusModel):
    data: UserResponse


class UserCreateRequest(BaseModel):
    email: Str
    password: Str
    firstname: Str
    age: Int16
    gender: Str
    height: Int16()
    is_smoke: bool
    hobbies: Str
    created_at: datetime


class UserUpdateRequest(UserCreateRequest):
    ...
