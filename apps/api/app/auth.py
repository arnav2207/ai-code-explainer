import logging
import time

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import get_settings

logger = logging.getLogger(__name__)

security = HTTPBearer()

# Module-level JWKS cache: refreshed at most once per hour.
_jwks_cache: dict = {"keys": [], "fetched_at": 0.0}
_JWKS_TTL_SECONDS = 3600


async def _get_jwks_keys() -> list[dict]:
    """Return cached JWKS keys, refreshing from Clerk if the cache has expired."""
    now = time.monotonic()
    if now - _jwks_cache["fetched_at"] < _JWKS_TTL_SECONDS and _jwks_cache["keys"]:
        return _jwks_cache["keys"]

    settings = get_settings()
    if not settings.clerk_jwks_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CLERK_JWKS_URL is not configured",
        )

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(settings.clerk_jwks_url)
            response.raise_for_status()
            keys = response.json().get("keys", [])
    except httpx.HTTPError as exc:
        logger.error("Failed to fetch Clerk JWKS: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch authentication keys",
        ) from exc

    _jwks_cache["keys"] = keys
    _jwks_cache["fetched_at"] = now
    return keys


async def verify_clerk_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """FastAPI dependency that validates a Clerk-issued RS256 JWT.

    Returns the decoded payload (dict) on success; raises HTTP 401 on failure.
    """
    keys = await _get_jwks_keys()
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            {"keys": keys},
            algorithms=["RS256"],
        )
    except JWTError as exc:
        logger.warning("JWT validation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return payload
