from http import HTTPStatus
from http import HTTPStatus
from pathlib import Path
from typing import Optional
from uuid import UUID

from fastapi import Response, UploadFile, File, Form
from funcy import invoke, first
from peewee_async import execute

from app.database import db_manager
from app.db_models import Photo
from app.responses import APIResponse
from app.settings import settings
from .utils import (
    response_model, get_or_404, set_attrs,
)
from ..models.photo import EnvelopedListOfPhotosResponse, EnvelopedPhotoResponse, PhotoUpdateRequest, PhotoResponse


@response_model(EnvelopedListOfPhotosResponse)
async def get_photos() -> Response:
    photo = await execute(Photo.select())
    return APIResponse(invoke(map(PhotoResponse.from_orm, photo), 'dict'))


@response_model(EnvelopedPhotoResponse, status_code=HTTPStatus.CREATED)
async def create_photo(user: UUID = Form(...), is_main:bool = Form(...), image: UploadFile = File(...)) -> Response:
    contents = await image.read()
    image_path = Path(settings.image_storage_name, str(user), image.filename)

    storage_path = Path(settings.project_dir, image_path)
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    with storage_path.open("wb") as f:
        f.write(contents)

    image_url = f'{settings.app_uri}://{settings.app_host}:{settings.app_port}/{image_path}'
    user_id = await execute(Photo.insert(user=user, is_main=is_main, url=image_url))

    photo = first(await execute(Photo.filter(id=user_id)))
    return APIResponse(
        PhotoResponse.from_orm(photo).dict(), status_code=HTTPStatus.CREATED
    )


@response_model(status_code=HTTPStatus.OK)
async def delete_photo(photo_id: UUID) -> Response:
    await get_or_404(Photo.select(), True)
    await execute(Photo.delete().where(Photo.id == photo_id))
    return APIResponse(status_code=HTTPStatus.NO_CONTENT)
