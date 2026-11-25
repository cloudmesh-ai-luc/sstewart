
"""JWT creation and validation utilities."""

from datetime import datetime, timedelta, timezone

import jwt

from app.services.config import get_auth_config


def create_access_token(operator_id: int) -> str:
    """Create a signed JWT for an authenticated operator."""

    config = get_auth_config()

    now = datetime.now(timezone.utc)

    expiration = now + timedelta(
        minutes=config["access_token_expire_minutes"]
    )

    payload = {
        "sub": str(operator_id),
        "iat": now,
        "exp": expiration,
    }

    token = jwt.encode(
        payload,
        config["secret_key"],
        algorithm=config["algorithm"],
    )

    return token


def decode_access_token(token: str) -> dict:
    """Validate a JWT and return its payload."""

    config = get_auth_config()

    payload = jwt.decode(
        token,
        config["secret_key"],
        algorithms=[config["algorithm"]],
        options={
            "require": ["sub", "iat", "exp"],
        },
    )

    return payload
