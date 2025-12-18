import os
import bcrypt
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional, Dict, Any
from dotenv import load_dotenv



# Load environment variables from .env
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a signed JWT access token.

    :param data: Payload to encode (e.g. {"sub": user_id})
    :param expires_delta: Optional custom expiry timedelta
    :return: JWT token as string
    """
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not set in environment variables")


    to_encode = data.copy()

    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return encoded_jwt

def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify a JWT token and return its payload.
    Raises HTTPException if token is invalid or expired.
    """
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not set in environment variables")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

def get_password_hash(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
