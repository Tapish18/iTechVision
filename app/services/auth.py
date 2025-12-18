from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils import verify_password,create_access_token


def login_user_service(
    login_in: LoginRequest,
    db: Session
) -> TokenResponse:
    """
    Verify user credentials and return JWT token.
    """
    try:
        user = db.query(User).filter(User.email == login_in.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(login_in.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )
        return TokenResponse(access_token=access_token)

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Authentication failed"
        )
