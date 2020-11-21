from http import HTTPStatus
import os
from starlette.responses import JSONResponse, Response

from .utils import (
    response_model, )


@response_model(status_code=HTTPStatus.OK)
def get_env_info():
    return JSONResponse(dict(os.environ.items()))