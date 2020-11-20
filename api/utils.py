import re
from typing import Union
from uuid import UUID

from fastapi.security import APIKeyCookie
from pydantic import BaseModel, ConstrainedInt, ConstrainedStr, Json, validator
from pydantic.color import Color, ColorType

from app.constants import MAX_INT, MAX_SHORT_INT
from app.settings import settings

# AUTH_SCHEME = APIKeyCookie(name=settings.auth_token_cookie_name, auto_error=False)


class Int32(ConstrainedInt):
    lt = MAX_INT
    gt = -1


class Int16(ConstrainedInt):
    lt = MAX_SHORT_INT
    gt = -1


class Str(ConstrainedStr):
    regex = re.compile(r'^[^\x00]*$')


class ShortStr(Str):
    max_length = 255


class SlugStr(ConstrainedStr):
    regex = re.compile(r'^[-a-zA-Z0-9_]+$')
    max_length = 255


UuidOrSlug = Union[UUID, SlugStr]


class ColorModel(Color):
    def __init__(self, value: Union[Color, ColorType]) -> None:
        if isinstance(value, Color):
            value = value.original()
        super().__init__(value)


class ShortObjectModel(BaseModel):
    id: UUID

    class Config:
        orm_mode = True

