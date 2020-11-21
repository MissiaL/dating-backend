from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database import connect_database, close_database
from app.logger.loguru_config import initialize_logger
from app.middleware import LoggingMiddleware
from app.routers import api_router, probes_router
from app.settings import settings
from cli import cli

app = FastAPI(title=settings.app_name,
              debug=settings.debug)

app.include_router(api_router)
app.include_router(probes_router)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


initialize_logger()

@app.on_event('startup')
async def on_startup() -> None:
    await connect_database()


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_database()


if __name__ == '__main__':
    cli()
