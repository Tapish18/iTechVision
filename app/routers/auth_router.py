from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.utils import verify_password, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

from app.services.auth import login_user_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    login_in: LoginRequest,
    response: Response,  # Inject FastAPI response object
    db: Session = Depends(get_db)
):
    """
    Authenticate user, return JWT token, and set Authorization header.
    """
    try:
        token_response = login_user_service(login_in, db)

        # Set the Authorization header
        response.headers["Authorization"] = f"Bearer {token_response.access_token}"

        return token_response

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during login"
        )

