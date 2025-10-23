from fastapi import Depends, HTTPException
from src.apps.auth.jwt import decode_jwt
from typing import Any


def require_groups(*allowed_groups: str):
    async def dependency(claims: dict[str, Any] = Depends(decode_jwt)):
        user_groups = set(claims.get("groups", []))

        if not user_groups.intersection(allowed_groups):
            raise HTTPException(status_code=403, detail="User does not belong to any of the allowed groups")
        return claims

    return dependency
