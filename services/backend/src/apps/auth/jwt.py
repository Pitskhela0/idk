from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.algorithms import RSAAlgorithm
from src.config import get_config
from src.apps.auth.jwks import get_jwks
from typing import Any
import jwt


config = get_config()

oauth2_scheme = OAuth2PasswordBearer(f"https://login.microsoftonline.com/{config.azure_client_id}/oauth2/v2.0/token")

ISSUER = f"https://login.microsoftonline.com/{config.azure_tenant_id}/v2.0"


async def get_signing_key(token_kid: str):
    jwks = await get_jwks()

    for key in jwks:
        if key.get('kid') == token_kid:
            return RSAAlgorithm.from_jwk(key)

    raise HTTPException(401, detail="Invalid token: Unknown 'kid'")


async def decode_jwt(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    header = jwt.get_unverified_header(token)
    kid = header.get('kid')

    if not kid:
        raise HTTPException(401, detail="Token header missing 'kid'")

    public_key = await get_signing_key(kid)

    try:
        payload = jwt.decode(
            token,
            key=public_key,
            algorithms=["RS256"],
            audience=config.azure_client_id,
            issuer=ISSUER,
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Expired token")

    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Invalid token")