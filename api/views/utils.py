import json
from datetime import datetime, timedelta
from http import HTTPStatus
from json import JSONDecodeError
from typing import Any, Callable, Dict, Iterator, List, Optional, Sized, Type

import jwt
from fastapi import Depends, Response
from fastapi.security import APIKeyCookie
from funcy import contextmanager, first
from jwt import ExpiredSignatureError, PyJWTError
from peewee import ModelSelect
from peewee_async import count, execute, prefetch
from pydantic import BaseModel

from app.database import BaseModel as PeeweeModel
from app.exceptions import BadRequest, NotFound, Unauthorized
from app.settings import settings

# AUTH_SCHEME = APIKeyCookie(name=settings.auth_token_cookie_name, auto_error=False)
# SOCIAL_AUTH_SCHEME = APIKeyCookie(
#     name=settings.social_auth_token_cookie_name, auto_error=False
# )


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


# def check_correct_ordering(orders: Sized) -> None:
#     correct_orders_sequence = range(1, len(orders) + 1)
#     if sorted(orders) != list(correct_orders_sequence):  # type: ignore
#         raise BadRequest('Order of objects should start with 1 and increase by 1')
#
#
# # have to have separate validators from schema
# # because pydantic can't handle async validators :( what a pity!
# async def check_existence(model: Type[PeeweeModel], field: str, **params: Any) -> None:
#     exists = not (await count(model.filter(**params)))
#     await field_check(exists, field, 'invalid', len(params))
#
#
# async def check_uniqueness(
#     model: Type[PeeweeModel], field: str, exclude_obj: PeeweeModel = None, **params: Any
# ) -> None:
#     query = model.filter(**params)
#     if exclude_obj:
#         query = query.where(~(model.id == exclude_obj.id))
#     non_unique = await count(query)
#     await field_check(non_unique, field, 'not unique', len(params))
#
#
# async def field_check(condition: bool, field: str, msg: str, num: int) -> None:
#     if condition:
#         verb = 'are' if num > 1 else 'is'
#         raise BadRequest(f'{field} {verb} {msg}')
#
#
# async def get_or_404(
#     query: ModelSelect,
#     *conditions: Any,
#     prefetches: Optional[Any] = None,
#     **filters: Any,
# ) -> PeeweeModel:
#     if conditions:
#         query = query.where(*conditions)
#     elif filters:
#         query = query.filter(**filters)
#
#     query = prefetch(query, *prefetches) if prefetches else execute(query)
#
#     obj = first(await query)
#     if obj is None:
#         raise NotFound
#     return obj  # type: ignore
#
#
# def set_attrs(obj: Any, **attrs: Any) -> Any:
#     for key, value in attrs.items():
#         setattr(obj, key, value)
#     return obj
#
#
# class User(BaseModel):
#     is_admin: bool = False
#     social_id: Optional[int]
#
#     @property
#     def is_authenticated(self) -> bool:
#         return self.is_admin or self.social_id is not None
#
#
# # def get_user(
# #     admin_token: Optional[str] = Depends(AUTH_SCHEME),
# #     student_token: Optional[str] = Depends(SOCIAL_AUTH_SCHEME),
# # ) -> User:
# #     user_data: Dict[str, Any] = dict()
# #
# #     with handle_decode_errors():
# #         user_data['social_id'] = student_token and get_student_social_id(student_token)
# #
# #     # Admin token can be expired. This is shouldn't affect student user-flows.
# #     with handle_decode_errors(reraise=user_data.get('social_id', None) is None):
# #         user_data['is_admin'] = admin_token is not None and is_admin_token(admin_token)
# #
# #     return User(**user_data)
#
#
# @contextmanager
# def handle_decode_errors(reraise: bool = True) -> Iterator:
#     try:
#         yield
#     except ValueError as e:
#         if reraise:
#             raise Unauthorized(str(e)) from e
#
#
# def is_admin_token(admin_token: str) -> bool:
#     return bool(decode_token(admin_token, settings.jwt_secret, ['HS256']))
#
#
# def get_student_social_id(student_token: str) -> int:
#     student_info = decode_token(student_token, settings.social_jwt_key, ['ES256'])
#     return int(student_info['social_id'])
#
# #
# # AUTH_USER = Depends(get_user)
#
#
# def auth_user_required(user: User = AUTH_USER) -> User:
#     if user.is_authenticated:
#         return user
#     else:
#         raise Unauthorized('Auth token is required')
#
#
# AUTH_USER_REQUIRED = Depends(auth_user_required)
#
#
# def student_required(user: User = AUTH_USER_REQUIRED) -> User:
#     if user.social_id:
#         return user
#     else:
#         raise Unauthorized()
#
#
# def admin_required(user: User = AUTH_USER_REQUIRED) -> User:
#     if user.is_admin:
#         return user
#     else:
#         raise Unauthorized()
#
#
# ADMIN_USER_REQUIRED = Depends(admin_required)
# STUDENT_REQUIRED = Depends(student_required)
#
#
# def make_access_token(username: str) -> str:
#     data = {'username': username, 'exp': get_token_expiration_date()}
#     try:
#         return encode_token(data).decode()
#     except PyJWTError as e:
#         raise BadRequest(str(e))
#
#
# def get_token_expiration_date() -> datetime:
#     return datetime.utcnow() + timedelta(days=settings.auth_token_expiration_days)
#
#
# def encode_token(data: dict) -> bytes:
#     return jwt.encode(data, settings.jwt_secret, algorithm='HS256')
#
#
# def decode_token(token: str, secret: str, algorithms: List[str]) -> dict:
#     try:
#         return jwt.decode(token, secret, algorithms=algorithms)
#     except ExpiredSignatureError:
#         raise ValueError('Expired access token')
#     except PyJWTError:
#         raise ValueError('Bad access token')
#
#
# def validate_custom_config(config: str) -> dict:
#     try:
#         return json.loads(config)  # type: ignore
#     except JSONDecodeError as e:
#         # sentence is half-finished because of the way errors are formatted later
#         raise ValueError('is invalid JSON') from e
