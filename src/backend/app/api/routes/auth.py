
"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_operator
from app.database import get_db
from app.models import Operator
from app.services.security import verify_password
from app.services.tokens import create_access_token


router = APIRouter()


# --------------------------------------------------
# Request and response schemas
# --------------------------------------------------

class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OperatorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str
    is_active: bool


# --------------------------------------------------
# Authentication endpoints
# --------------------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    """Authenticate an operator and return a JWT."""

    # Find the operator by email.
    stmt = select(Operator).where(
        Operator.email == payload.email
    )

    operator = db.execute(stmt).scalar_one_or_none()

    # Reject invalid credentials.
    if operator is None or not verify_password(
        payload.password,
        operator.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Reject disabled accounts.
    if not operator.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate an access token.
    access_token = create_access_token(operator.id)

    return TokenResponse(
        access_token=access_token,
    )


@router.get(
    "/me",
    response_model=OperatorRead,
)
def get_me(
    current_operator: Operator = Depends(get_current_operator),
):
    """Return the currently authenticated operator."""

    return current_operator
