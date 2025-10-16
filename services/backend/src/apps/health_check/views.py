import logging
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.config import config
from src.apps.health_check.dto import HealthOut
from src.apps.health_check.service import HealthCheckService, Probe, ProbeResult, UptimeCheck

logger = logging.getLogger(__name__)


async def health_check_handler(
    probe: Probe,
    health_check: HealthCheckService = Depends(),
):
    probe_result: ProbeResult = await health_check.run_probe(probe)
    return JSONResponse(
        content=jsonable_encoder(
            HealthOut(
                status=probe_result.status.name,
                version=config.app_version,
                checks=probe_result.checks,
            )
        ),
        status_code=probe_result.status.code,
        media_type="application/health+json",
    )


LIVENESS_PROBE = Probe(
    name="live",
    checks=[
        UptimeCheck(),
    ],
)
