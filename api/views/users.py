from http import HTTPStatus

from fastapi import Response

from app.responses import APIResponse
from .utils import (
    # User,
    response_model,
)
from ..models.user import EnvelopedListOfUsersResponse, EnvelopedUserResponse, UserCreateRequest, UserUpdateRequest


@response_model(EnvelopedListOfUsersResponse)
async def get_users() -> Response:
    return APIResponse({})


@response_model(EnvelopedUserResponse, status_code=HTTPStatus.CREATED)
async def create_user(data: UserCreateRequest) -> Response:
    return APIResponse({})


@response_model(EnvelopedUserResponse, status_code=HTTPStatus.OK)
async def update_user(user_id: int, data: UserUpdateRequest) -> Response:
    return APIResponse({})


@response_model(status_code=HTTPStatus.OK)
async def delete_user(user_id: int) -> Response:
    return APIResponse({})