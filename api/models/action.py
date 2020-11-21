from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from uuid import UUID

from api.models.user import ShortUserResponse
from app.response_models import ListModel, StatusModel


class ActionResponse(BaseModel):
    id: UUID
    user: ShortUserResponse
    like_to_user: Optional[ShortUserResponse]
    dislike_to_user: Optional[ShortUserResponse]
    created_at: datetime

    class Config:
        orm_mode = True


class EnvelopedListOfActionsResponse(ListModel):
    data: List[ActionResponse]


class EnvelopedActionResponse(StatusModel):
    data: ActionResponse


class ActionCreateRequest(BaseModel):
    user: UUID
    like_to_user: Optional[UUID]
    dislike_to_user: Optional[UUID]


class ActionUpdateRequest(ActionCreateRequest):
    user: UUID
    like_to_user: Optional[UUID]
    dislike_to_user: Optional[UUID]
