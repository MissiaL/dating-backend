from http import HTTPStatus

from fastapi import Response

from app.responses import APIResponse
from .utils import (
    response_model,
)
from ..models.cost import EnvelopedListOfCostsResponse, EnvelopedCostResponse, CostCreateRequest, CostUpdateRequest


@response_model(EnvelopedListOfCostsResponse)
async def get_costs() -> Response:
    return APIResponse({})


@response_model(EnvelopedCostResponse, status_code=HTTPStatus.CREATED)
async def create_cost(data: CostCreateRequest) -> Response:
    return APIResponse({})


@response_model(EnvelopedCostResponse, status_code=HTTPStatus.OK)
async def update_cost(cost_id: int, data: CostUpdateRequest) -> Response:
    return APIResponse({})


@response_model(status_code=HTTPStatus.OK)
async def delete_cost(cost_id: int) -> Response:
    return APIResponse({})