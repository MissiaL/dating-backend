from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from api.models.user import ShortUserResponse
from api.utils import Str
from app.response_models import ListModel, StatusModel


class MessageResponse(BaseModel):
    id: UUID
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
    user: UUID
    to_user: UUID
    text: Str


class MessageUpdateRequest(BaseModel):
    user: UUID
    to_user: Optional[UUID]
    text: Optional[Str]
