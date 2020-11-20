import logging.config
import sys
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable

from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.logger.logging_config import LOGCONFIG
from app.logger.sinks import TJBaseLogSink, TJRequestLogSink
from app.settings import settings

LOG_LEVELS_MAP = (
    (60, 'FATAL'),
    (50, 'ERROR'),
    (40, 'WARNING'),
    (30, 'INFO'),
    (20, 'DEBUG'),
    (10, 'TRACE'),
)


def initialize_logger() -> None:
    # Configure regular logging, and run logs of third-party
    # libraries through our sinks.
    logging.config.dictConfig(LOGCONFIG)

    # deletes preconfigured sinks
    logger.remove()

    if settings.debug:
        logger.add(
            sys.stderr,
            level='DEBUG',
            format='{level}: {time} [{name}] {message} {extra}',
            backtrace=True,
        )
    else:
        # Logger for request messages
        logger.add(
            TJRequestLogSink(),
            level='INFO',
            filter=lambda record: record['extra'].get('request', None),
        )
        # Logger for system messages
        logger.add(
            TJBaseLogSink(),
            level='INFO',
            filter=lambda record: record['extra'].get('system', None),
        )


def error_logger_handler(
    func: Callable[[Any, Request, Exception], JSONResponse]
) -> Callable:
    @wraps(func)
    def wrapper(self: object, request: Request, exc: Exception) -> JSONResponse:
        status_code = getattr(exc, 'status_code', HTTPStatus.INTERNAL_SERVER_ERROR)

        request.state.logger = request.state.logger.bind(
            response={'status_code': status_code}
        )
        request.state.logger.exception(str(exc))
        return func(self, request, exc)

    return wrapper
