from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import UploadFile, File
from pydantic import BaseModel, AnyUrl

from api.models.user import ShortUserResponse
from app.response_models import ListModel, StatusModel


class PhotoResponse(BaseModel):
    id: UUID
    user: ShortUserResponse
    is_main: bool
    url: str
    created_at: datetime

    class Config:
        orm_mode = True


class EnvelopedListOfPhotosResponse(ListModel):
    data: List[PhotoResponse]


class EnvelopedPhotoResponse(StatusModel):
    data: PhotoResponse


class PhotoCreateRequest(BaseModel):
    user: UUID
    is_main: bool


class PhotoUpdateRequest(BaseModel):
    user: UUID
    is_main: Optional[bool]
