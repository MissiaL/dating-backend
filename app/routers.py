from fastapi import APIRouter

from app.routes import api_routes

api_router = APIRouter()
api_router.routes.extend(api_routes)
