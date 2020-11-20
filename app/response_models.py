from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Statuses(str, Enum):
    OK = 'ok'
    ERROR = 'error'


class ErrorDescription(BaseModel):
    code: str
    message: str


class StatusModel(BaseModel):
    status = Statuses.OK


class ListModel(StatusModel):
    count: Optional[int]


class PaginateListModel(ListModel):
    limit: Optional[int]
    offset: Optional[int]


class ErrorModel(StatusModel):
    status = Statuses.ERROR
    error: ErrorDescription
