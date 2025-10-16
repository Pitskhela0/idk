from fastapi import Depends, HTTPException
from src.apps.auth.jwt import decode_jwt
from typing import Any


def require_roles(*allowed_roles: str):
    async def dependency(claims: dict[str, Any] = Depends(decode_jwt)):
        user_roles = set(claims.get("roles", []))

        if not user_roles.intersection(allowed_roles):
            raise HTTPException(status_code=403, detail="Insufficient role")
        return claims

    return dependency


def require_scopes(*allowed_scopes: str):
    async def dependency(claims: dict[str, Any] = Depends(decode_jwt)):
        user_scopes = set(claims.get("scope", "").split())

        if not user_scopes.intersection(allowed_scopes):
            raise HTTPException(status_code=403, detail="Insufficient scope")
        return claims

    return dependency
