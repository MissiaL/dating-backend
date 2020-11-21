from http import HTTPStatus
from uuid import UUID

from fastapi import Response
from funcy import invoke, first
from peewee_async import execute

from app.database import db_manager
from app.db_models import Cost
from app.responses import APIResponse
from .utils import (
    response_model, get_or_404, set_attrs,
)
from ..models.cost import EnvelopedListOfCostsResponse, EnvelopedCostResponse, CostCreateRequest, CostUpdateRequest, CostResponse


@response_model(EnvelopedListOfCostsResponse)
async def get_costs() -> Response:
    costs = await execute(Cost.select())
    return APIResponse(invoke(map(CostResponse.from_orm, costs), 'dict'))


@response_model(EnvelopedCostResponse, status_code=HTTPStatus.CREATED)
async def create_cost(data: CostCreateRequest) -> Response:
    cost_id = await execute(Cost.insert(**data.dict()))
    cost = first(await execute(Cost.filter(id=cost_id)))
    return APIResponse(
        CostResponse.from_orm(cost).dict(), status_code=HTTPStatus.CREATED
    )


@response_model(EnvelopedCostResponse, status_code=HTTPStatus.OK)
async def update_cost(cost_id: UUID, data: CostUpdateRequest) -> Response:
    cost = await get_or_404(Cost.select(), id=cost_id)

    update_data = data.dict(exclude_unset=True)

    cost = set_attrs(cost, **update_data)
    await db_manager.update(cost)
    return APIResponse(CostResponse.from_orm(cost).dict())


@response_model(status_code=HTTPStatus.OK)
async def delete_cost(cost_id: UUID) -> Response:
    await get_or_404(Cost.select(), True)
    await execute(Cost.delete().where(Cost.id == cost_id))
    return APIResponse(status_code=HTTPStatus.NO_CONTENT)