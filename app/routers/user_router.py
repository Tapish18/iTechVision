from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.services.user import create_user_service,get_user_details_service,update_user_service,delete_user_service,get_all_users_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Delegates DB insertion and password hashing to the service layer.
    """
    # Call the service function
    user = create_user_service(user_in, db)
    return user

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get details of a user by user_id.
    """
    user_details = get_user_details_service(user_id,db)  
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    return user_details


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all users with pagination.
    """
    try:
        return get_all_users_service(db, skip, limit)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while fetching users"
        )

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user details by user ID.
    """
    try:
        return update_user_service(user_id, user_in, db)
    except HTTPException:
        # pass through service-level HTTP errors
        raise
    except Exception:
        # safeguard (rarely hit)
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while updating user"
        )

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user by user ID.
    """
    try:
        delete_user_service(user_id, db)
        return {"detail": "User deleted successfully"}
    except HTTPException:
        # pass through service-level HTTP errors
        raise
    except Exception:
        # safeguard
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while deleting user"
        )

