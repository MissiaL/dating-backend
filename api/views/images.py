from http import HTTPStatus
from http import HTTPStatus
from pathlib import Path
from uuid import UUID

from fastapi import Response
from starlette.responses import FileResponse

from app.settings import settings
from .utils import (
    response_model, )


@response_model(status_code=HTTPStatus.OK)
async def get_image(user_id: UUID, filename: str):
    image = Path(settings.images_dir, str(user_id), filename)
    response = FileResponse(image.absolute())
    return response