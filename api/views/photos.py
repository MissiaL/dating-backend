from http import HTTPStatus

from fastapi import Response

from app.responses import APIResponse
from .utils import (
    response_model,
)
from ..models.photo import EnvelopedListOfPhotosResponse, EnvelopedPhotoResponse, PhotoCreateRequest, PhotoUpdateRequest


@response_model(EnvelopedListOfPhotosResponse)
async def get_photos() -> Response:
    return APIResponse({})


@response_model(EnvelopedPhotoResponse, status_code=HTTPStatus.CREATED)
async def create_photo(data: PhotoCreateRequest) -> Response:
    return APIResponse({})


@response_model(EnvelopedPhotoResponse, status_code=HTTPStatus.OK)
async def update_photo(photo_id: int, data: PhotoUpdateRequest) -> Response:
    return APIResponse({})


@response_model(status_code=HTTPStatus.OK)
async def delete_photo(photo_id: int) -> Response:
    return APIResponse({})