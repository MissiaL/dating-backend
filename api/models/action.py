from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.response_models import ListModel, StatusModel


class ActionResponse(BaseModel):
    user: int
    like_to_user: int
    dislike_to_user: int
    created_at: datetime


class EnvelopedListOfActionsResponse(ListModel):
    data: List[ActionResponse]


class EnvelopedActionResponse(StatusModel):
    data: ActionResponse


class ActionCreateRequest(BaseModel):
    user: int
    like_to_user: int
    dislike_to_user: int


class ActionUpdateRequest(ActionCreateRequest):
    ...
