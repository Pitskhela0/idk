from fastapi import APIRouter, status
from functools import partial

from src.apps.health_check.views import health_check_handler, LIVENESS_PROBE
from src.apps.health_check.dto import HealthOut

api_v0_router = APIRouter()

api_v0_router.add_api_route(
    path="/health/live",
    endpoint=partial(health_check_handler, LIVENESS_PROBE),
    response_model=HealthOut,
    methods=["GET"],
    summary="Probe live",
    tags=["Telemetry"],
    responses={
        status.HTTP_200_OK: {
            "description": "Indicates that apps is healthy",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Indicates that apps is unhealthy",
        },
    },
)
