

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.logger = logger.bind(
            request={
                'id': request.headers.get('x-request-id', ''),
                'method': request.method,
                'path': request.url.path,
            },
            session_id=request.headers.get('x-session-id', ''),
        )

        response = await call_next(request)
        request.state.logger = request.state.logger.bind(
            response={'status_code': response.status_code}
        )
        request.state.logger.info(f'response:{response.status_code}')
        return response


