
"""FastAPI dependencies for authentication and authorization."""

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Operator
from app.services.tokens import decode_access_token


# Extract Bearer tokens without automatically raising FastAPI's
# default authentication error.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_operator(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> Operator:
    """Validate the JWT and return the authenticated operator."""

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Ensure the request includes a Bearer token.
    if credentials is None:
        raise unauthorized

    # Validate the token signature and expiration.
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.InvalidTokenError:
        raise unauthorized

    # Extract the operator ID from the token subject.
    subject = payload.get("sub")

    if not isinstance(subject, str) or not subject.isdigit():
        raise unauthorized

    operator_id = int(subject)

    if operator_id <= 0:
        raise unauthorized

    # Retrieve the operator from MariaDB.
    operator = db.get(Operator, operator_id)

    if operator is None or not operator.is_active:
        raise unauthorized

    return operator



def require_roles(*allowed_roles: str):
    """Require an authenticated operator with an allowed role."""

    def role_checker(
        current_operator: Operator = Depends(get_current_operator),
    ) -> Operator:

        if current_operator.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_operator

    return role_checker
