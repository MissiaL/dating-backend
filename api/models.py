from datetime import datetime
from typing import List

from pydantic import BaseModel

from api.utils import Str, Int16
from app.response_models import ListModel, StatusModel


class MessageResponse(BaseModel):
    user: int
    to_user: int
    text: Str
    created_at: datetime

