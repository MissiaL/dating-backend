from typing import Any, Dict, Iterable

from fastapi.routing import APIRoute

from app.response_models import ErrorModel
from app.routes import api_paths, services_paths


def make_routes(
    spec: Dict[str, Any], include_in_schema: bool = True
) -> Iterable[APIRoute]:
    responses = {
        '4xx': {
            "model": ErrorModel,
            "description": "Bad request",
            'content': {'application/json': {}},
        }
    }
    for tag, routes in spec.items():
        for route in routes:
            path, method, func, *params = route

            name = params[0] if params else func.__name__
            status_code = params[1] if len(params) > 1 else 200

            response_model = getattr(func, 'response_model', None)
            response_class = getattr(func, 'response_class', None)
            response_status_code = getattr(func, 'response_status_code', status_code)
            deprecated = 'deprecated' in name

            yield APIRoute(
                path,
                func,
                name=name,
                methods=[method],
                tags=[tag],
                operation_id=name,
                response_model=response_model,
                responses=responses,  # type: ignore
                status_code=response_status_code,
                response_class=response_class,
                deprecated=deprecated,
                include_in_schema=include_in_schema,
            )


api_routes = make_routes(api_paths.paths)
services_routes = make_routes(services_paths.paths, include_in_schema=False)