from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from api.utils import Str, Int16
from app.response_models import ListModel, StatusModel


class CostResponse(BaseModel):
    user: int
    name: Str
    price: Int16
    created_at: datetime
    

class EnvelopedListOfCostsResponse(ListModel):
    data: List[CostResponse]


class EnvelopedCostResponse(StatusModel):
    data: CostResponse


class CostCreateRequest(BaseModel):
    user: int
    name: Str
    price: Int16

class CostUpdateRequest(CostCreateRequest):
    ...
