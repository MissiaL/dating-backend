from http import HTTPStatus

from fastapi import Response
from funcy import invoke, first
from peewee_async import execute

from app.database import db_manager
from app.db_models import Photo
from app.responses import APIResponse
from .utils import (
    response_model, get_or_404, set_attrs,
)
from ..models.photo import EnvelopedListOfPhotosResponse, EnvelopedPhotoResponse, PhotoCreateRequest, \
    PhotoUpdateRequest, PhotoResponse


@response_model(EnvelopedListOfPhotosResponse)
async def get_photos() -> Response:
    photo = await execute(Photo.select())
    return APIResponse(invoke(map(PhotoResponse.from_orm, photo), 'dict'))


@response_model(EnvelopedPhotoResponse, status_code=HTTPStatus.CREATED)
async def create_photo(data: PhotoCreateRequest) -> Response:
    user_id = await execute(Photo.insert(**data.dict()))
    user = first(await execute(Photo.filter(id=user_id)))
    return APIResponse(
        PhotoResponse.from_orm(user).dict(), status_code=HTTPStatus.CREATED
    )


@response_model(EnvelopedPhotoResponse, status_code=HTTPStatus.OK)
async def update_photo(photo_id: int, data: PhotoUpdateRequest) -> Response:
    user = await get_or_404(Photo.select(), True)

    update_data = data.dict(exclude_unset=True)

    course = set_attrs(user, **update_data)
    await db_manager.update(course)
    return APIResponse(PhotoResponse.from_orm(course).dict())


@response_model(status_code=HTTPStatus.OK)
async def delete_photo(photo_id: int) -> Response:
    await get_or_404(Photo.select(), True)
    await execute(Photo.delete().where(Photo.id == photo_id))
    return APIResponse(status_code=HTTPStatus.NO_CONTENT)
