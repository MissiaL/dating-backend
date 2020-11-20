from starlette.requests import Request
from starlette.responses import JSONResponse, Response


async def probe_handler(request: Request) -> Response:
    return JSONResponse(status_code=204)


paths = {
    'probes': [
        ('/livenessProbe/', 'GET', probe_handler, 'liveness', 204),
        ('/readinessProbe/', 'GET', probe_handler, 'readiness', 204),
    ]
}
