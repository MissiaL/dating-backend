from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from api.models.user import ShortUserResponse
from api.utils import Str
from app.response_models import ListModel, StatusModel


class MessageResponse(BaseModel):
    user: ShortUserResponse
    to_user: ShortUserResponse
    text: Str
    created_at: datetime

    class Config:
        orm_mode = True


class EnvelopedListOfMessagesResponse(ListModel):
    data: List[MessageResponse]


class EnvelopedMessageResponse(StatusModel):
    data: MessageResponse


class MessageCreateRequest(BaseModel):
    user: int
    to_user: int
    text: Str


class MessageUpdateRequest(BaseModel):
    user: int
    to_user: Optional[int]
    text: Optional[Str]
