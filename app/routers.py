from fastapi import APIRouter

from app.routes import api_routes, services_routes

api_router = APIRouter()
api_router.routes.extend(api_routes)

probes_router = APIRouter()
probes_router.routes.extend(services_routes)