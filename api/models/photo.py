from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel, AnyUrl

from app.response_models import ListModel, StatusModel


class PhotoResponse(BaseModel):
    user: int
    is_main: bool
    link: AnyUrl
    created_at: datetime

    class Config:
        orm_mode = True


class EnvelopedListOfPhotosResponse(ListModel):
    data: List[PhotoResponse]


class EnvelopedPhotoResponse(StatusModel):
    data: PhotoResponse


class PhotoCreateRequest(BaseModel):
    user: int
    is_main: bool
    image: bytes


class PhotoUpdateRequest(BaseModel):
    user: int
    is_main: Optional[bool]
    image: Optional[bytes]
