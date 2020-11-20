from http import HTTPStatus

from fastapi import Response
from funcy import first, invoke
from peewee_async import execute

from app.database import db_manager
from app.db_models import User
from app.responses import APIResponse
from .utils import (
    # User,
    response_model, get_or_404, set_attrs,
)
from ..models.user import EnvelopedListOfUsersResponse, EnvelopedUserResponse, UserCreateRequest, UserUpdateRequest, \
    UserResponse


@response_model(EnvelopedListOfUsersResponse)
async def get_users() -> Response:
    users = await execute(User.select())
    return APIResponse(invoke(map(UserResponse.from_orm, users), 'dict'))



@response_model(EnvelopedUserResponse, status_code=HTTPStatus.CREATED)
async def create_user(data: UserCreateRequest) -> Response:
    user_id = await execute(User.insert(**data.dict()))
    user = first(await execute(User.filter(id=user_id)))
    return APIResponse(
        UserResponse.from_orm(user).dict(), status_code=HTTPStatus.CREATED
    )


@response_model(EnvelopedUserResponse, status_code=HTTPStatus.OK)
async def update_user(user_id: int, data: UserUpdateRequest) -> Response:
    user = await get_or_404(User.select(), id=user_id)

    update_data = data.dict(exclude_unset=True)

    course = set_attrs(user, **update_data)
    await db_manager.update(course)
    return APIResponse(UserResponse.from_orm(course).dict())


@response_model(status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int) -> Response:
    await get_or_404(User.select(), id=user_id)
    await execute(User.delete().where(User.id == user_id))
    return APIResponse(status_code=HTTPStatus.NO_CONTENT)