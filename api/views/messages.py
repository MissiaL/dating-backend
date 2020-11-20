from http import HTTPStatus

from fastapi import Response

from app.responses import APIResponse
from .utils import (
    response_model,
)
from ..models.message import EnvelopedListOfMessagesResponse, EnvelopedMessageResponse, MessageCreateRequest, MessageUpdateRequest


@response_model(EnvelopedListOfMessagesResponse)
async def get_messages() -> Response:
    return APIResponse({})


@response_model(EnvelopedMessageResponse, status_code=HTTPStatus.CREATED)
async def create_message(data: MessageCreateRequest) -> Response:
    return APIResponse({})


@response_model(EnvelopedMessageResponse, status_code=HTTPStatus.OK)
async def update_message(message_id: int, data: MessageUpdateRequest) -> Response:
    return APIResponse({})


@response_model(status_code=HTTPStatus.OK)
async def delete_message(message_id: int) -> Response:
    return APIResponse({})