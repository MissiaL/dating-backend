from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from api.models.user import ShortUserResponse
from api.utils import Str, Int16
from app.response_models import ListModel, StatusModel


class CostResponse(BaseModel):
    user: ShortUserResponse
    name: str
    price: str
    created_at: datetime

    class Config:
        orm_mode = True


class EnvelopedListOfCostsResponse(ListModel):
    data: List[CostResponse]


class EnvelopedCostResponse(StatusModel):
    data: CostResponse


class CostCreateRequest(BaseModel):
    user: int
    name: str
    price: int


class CostUpdateRequest(BaseModel):
    user: int
    name: Optional[str]
    price: Optional[int]
