from http import HTTPStatus

from fastapi import Response
from funcy import invoke, first
from peewee_async import execute

from app.database import db_manager
from app.db_models import Action
from app.responses import APIResponse
from .utils import (
    response_model, get_or_404, set_attrs,
)
from ..models.action import EnvelopedListOfActionsResponse, EnvelopedActionResponse, ActionCreateRequest, \
    ActionUpdateRequest, ActionResponse


@response_model(EnvelopedListOfActionsResponse)
async def get_actions() -> Response:
    actions = await execute(Action.select())
    return APIResponse(invoke(map(ActionResponse.from_orm, actions), 'dict'))

@response_model(EnvelopedActionResponse, status_code=HTTPStatus.CREATED)
async def create_action(data: ActionCreateRequest) -> Response:
    action_id = await execute(Action.insert(**data.dict()))
    action = first(await execute(Action.filter(id=action_id)))
    return APIResponse(
        ActionResponse.from_orm(action).dict(), status_code=HTTPStatus.CREATED
    )



@response_model(EnvelopedActionResponse, status_code=HTTPStatus.OK)
async def update_action(action_id: int, data: ActionUpdateRequest) -> Response:
    action = await get_or_404(Action.select(), id=action_id)

    update_data = data.dict(exclude_unset=True)

    action = set_attrs(action, **update_data)
    await db_manager.update(action)
    return APIResponse(ActionResponse.from_orm(action).dict())



@response_model(status_code=HTTPStatus.OK)
async def delete_action(action_id: int) -> Response:
    await get_or_404(Action.select(), True)
    await execute(Action.delete().where(Action.id == action_id))
    return APIResponse(status_code=HTTPStatus.NO_CONTENT)