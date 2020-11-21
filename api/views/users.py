from http import HTTPStatus
from uuid import UUID

from fastapi import Depends,  HTTPException
from fastapi.security import HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi import Response
from fastapi.security import HTTPBasic
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

security = HTTPBasic()


async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = await get_or_404(User.select(), email=credentials.username)

    if credentials.password != user.password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.id


@response_model(EnvelopedListOfUsersResponse)
async def get_users() -> Response:
    users = await execute(User.select())
    return APIResponse(invoke(map(UserResponse.from_orm, users), 'dict'))


@response_model(EnvelopedUserResponse)
async def get_user(user_id: UUID = Depends(get_current_username)) -> Response:
    user = await get_or_404(User.select(), id=user_id)
    return APIResponse(
        UserResponse.from_orm(user).dict(), status_code=HTTPStatus.OK
    )

@response_model(EnvelopedUserResponse, status_code=HTTPStatus.CREATED)
async def create_user(data: UserCreateRequest) -> Response:
    user_id = await execute(User.insert(**data.dict()))
    user = first(await execute(User.filter(id=user_id)))
    return APIResponse(
        UserResponse.from_orm(user).dict(), status_code=HTTPStatus.CREATED
    )


@response_model(EnvelopedUserResponse, status_code=HTTPStatus.OK)
async def update_user(user_id: UUID, data: UserUpdateRequest) -> Response:
    user = await get_or_404(User.select(), id=user_id)

    update_data = data.dict(exclude_unset=True)

    course = set_attrs(user, **update_data)
    await db_manager.update(course)
    return APIResponse(UserResponse.from_orm(course).dict())


@response_model(status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: UUID) -> Response:
    await get_or_404(User.select(), id=user_id)
    await execute(User.delete().where(User.id == user_id))
    return APIResponse(status_code=HTTPStatus.NO_CONTENT)