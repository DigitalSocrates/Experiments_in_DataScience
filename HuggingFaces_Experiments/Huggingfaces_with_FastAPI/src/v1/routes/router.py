from fastapi import APIRouter

from src.v1.routes import prediction
from src.v1.routes import heartbeat

api_router = APIRouter()
api_router.include_router(heartbeat.router, tags=["health"], prefix="/health")
api_router.include_router(prediction.router, tags=["prediction"], prefix="/v1")
