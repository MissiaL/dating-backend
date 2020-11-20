from http import HTTPStatus

from fastapi import HTTPException


class ImproperlyConfigured(Exception):
    ...


class CustomHTTPException(HTTPException):
    status: HTTPStatus

    def __init__(self, message: str = ''):
        super().__init__(
            status_code=self.status.value, detail=message or self.status.phrase
        )


class Unauthorized(CustomHTTPException):
    status = HTTPStatus.UNAUTHORIZED


class NotFound(CustomHTTPException):
    status = HTTPStatus.NOT_FOUND


class BadRequest(CustomHTTPException):
    status = HTTPStatus.BAD_REQUEST


class ServerError(CustomHTTPException):
    status = HTTPStatus.INTERNAL_SERVER_ERROR


class ConflictError(CustomHTTPException):
    status = HTTPStatus.CONFLICT


class ForbiddenError(CustomHTTPException):
    status = HTTPStatus.FORBIDDEN
