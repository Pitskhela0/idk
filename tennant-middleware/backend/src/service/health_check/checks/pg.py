from dataclasses import dataclass
from datetime import UTC, datetime

from src.service.health_check.dto import CheckComponentType, CheckResult
from src.service.health_check.service import (
    Check,
    ProbeResultStatus,
    warn_status,
)


@dataclass
class PgCheck(Check):
    component_type: CheckComponentType = CheckComponentType.datastore

    async def __call__(self) -> CheckResult:
        check_result = warn_status

        return CheckResult(
            component_id=self.component_id,
            component_type=self.component_type,
            status=check_result.name,
            time=datetime.now(UTC).isoformat(),
            observed_value="database not used in this project",
        )
