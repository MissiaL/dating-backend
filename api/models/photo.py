from datetime import datetime
from typing import List

from pydantic import BaseModel, AnyUrl

from api.utils import Str
from app.response_models import ListModel, StatusModel


class PhotoResponse(BaseModel):
    user: int
    is_main: bool
    link: AnyUrl
    created_at: datetime


class EnvelopedListOfPhotosResponse(ListModel):
    data: List[PhotoResponse]


class EnvelopedPhotoResponse(StatusModel):
    data: PhotoResponse


class PhotoCreateRequest(BaseModel):
    user: int
    is_main: bool
    image: bytes


class PhotoUpdateRequest(PhotoCreateRequest):
    ...
