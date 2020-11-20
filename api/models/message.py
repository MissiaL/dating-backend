from datetime import datetime
from typing import List

from pydantic import BaseModel

from api.utils import Str
from app.response_models import ListModel, StatusModel


class MessageResponse(BaseModel):
    user: int
    to_user: int
    text: Str
    created_at: datetime


class EnvelopedListOfMessagesResponse(ListModel):
    data: List[MessageResponse]


class EnvelopedMessageResponse(StatusModel):
    data: MessageResponse


class MessageCreateRequest(BaseModel):
    user: int
    to_user: int
    text: Str
    created_at: datetime


class MessageUpdateRequest(MessageCreateRequest):
    ...
