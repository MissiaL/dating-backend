from http import HTTPStatus

from fastapi import Response

from app.responses import APIResponse
from .utils import (
    response_model,
)
from ..models.action import EnvelopedListOfActionsResponse, EnvelopedActionResponse, ActionCreateRequest, ActionUpdateRequest


@response_model(EnvelopedListOfActionsResponse)
async def get_actions() -> Response:
    return APIResponse({})


@response_model(EnvelopedActionResponse, status_code=HTTPStatus.CREATED)
async def create_action(data: ActionCreateRequest) -> Response:
    return APIResponse({})


@response_model(EnvelopedActionResponse, status_code=HTTPStatus.OK)
async def update_action(action_id: int, data: ActionUpdateRequest) -> Response:
    return APIResponse({})


@response_model(status_code=HTTPStatus.OK)
async def delete_action(action_id: int) -> Response:
    return APIResponse({})