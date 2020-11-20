from http import HTTPStatus
from typing import Any, Callable, Optional, Type

from fastapi import Response
from funcy import first
from peewee import ModelSelect
from peewee_async import execute, prefetch
from pydantic import BaseModel

from app.database import BaseModel as PeeweeModel
from app.exceptions import NotFound


def response_model(
    model: Optional[Type[BaseModel]] = None,
    status_code: int = HTTPStatus.OK,
    response_class: Optional[Type[Response]] = None,
) -> Callable:
    def inner(f: Callable) -> Callable:
        f.response_model = model  # type: ignore
        f.response_status_code = int(status_code)  # type: ignore
        f.response_class = response_class  # type: ignore
        return f

    return inner


async def get_or_404(
    query: ModelSelect,
    *conditions: Any,
    prefetches: Optional[Any] = None,
    **filters: Any,
) -> PeeweeModel:
    if conditions:
        query = query.where(*conditions)
    elif filters:
        query = query.filter(**filters)

    query = prefetch(query, *prefetches) if prefetches else execute(query)

    obj = first(await query)
    if obj is None:
        raise NotFound
    return obj  # type: ignore
#
#
def set_attrs(obj: Any, **attrs: Any) -> Any:
    for key, value in attrs.items():
        setattr(obj, key, value)
    return obj
