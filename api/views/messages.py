from http import HTTPStatus

from fastapi import Response
from funcy import invoke, first
from peewee_async import execute

from app.database import db_manager
from app.db_models import Message
from app.responses import APIResponse
from .utils import (
    response_model, get_or_404, set_attrs,
)
from ..models.message import EnvelopedListOfMessagesResponse, EnvelopedMessageResponse, MessageCreateRequest, \
    MessageUpdateRequest, MessageResponse


@response_model(EnvelopedListOfMessagesResponse)
async def get_messages() -> Response:
    messages = await execute(Message.select())
    return APIResponse(invoke(map(MessageResponse.from_orm, messages), 'dict'))


@response_model(EnvelopedMessageResponse, status_code=HTTPStatus.CREATED)
async def create_message(data: MessageCreateRequest) -> Response:
    message_id = await execute(Message.insert(**data.dict()))
    message = first(await execute(Message.filter(id=message_id)))
    return APIResponse(
        MessageResponse.from_orm(message).dict(), status_code=HTTPStatus.CREATED
    )


@response_model(EnvelopedMessageResponse, status_code=HTTPStatus.OK)
async def update_message(message_id: int, data: MessageUpdateRequest) -> Response:
    message = await get_or_404(Message.select(), id=message_id)

    update_data = data.dict(exclude_unset=True)

    message = set_attrs(message, **update_data)
    await db_manager.update(message)
    return APIResponse(MessageResponse.from_orm(message).dict())


@response_model(status_code=HTTPStatus.OK)
async def delete_message(message_id: int) -> Response:
    await get_or_404(Message.select(), True)
    await execute(Message.delete().where(Message.id == message_id))
    return APIResponse(status_code=HTTPStatus.NO_CONTENT)