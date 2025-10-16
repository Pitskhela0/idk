import httpx
import time
from typing import Any
from src.config import get_config


_cached_keys: list[dict[str, Any]] | None = None
_cached_at: float | None = None
_CACHE_TTL = 24 * 60 * 60 # 24 Hours. To be configured (Maybe move this variable to config file)


async def get_jwks() -> list[dict[str, Any]]:
    global _cached_keys, _cached_at

    now =  time.time()

    if _cached_keys and _cached_at and now - _cached_at < _CACHE_TTL:
        return _cached_keys

    async with httpx.AsyncClient() as client:
        resp = await client.get(get_config().azure_jwks_url)
        resp.raise_for_status()

        keys = resp.json().get('keys')
        if not keys:
            raise RuntimeError('JWKS endpoint did not return keys')

        _cached_keys = keys
        _cached_at = now

        return keys