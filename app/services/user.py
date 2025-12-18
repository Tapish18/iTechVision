from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User
from app.utils import get_password_hash
from app.schemas.user import UserCreate

def create_user_service(user_in: UserCreate, db: Session) -> User:
    hashed_password = get_password_hash(user_in.password)

    user = User(
        username=user_in.username,
        email=user_in.email,
        password=hashed_password
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="User creation failed")
    return user

def get_user_details_service(user_id: int, db: Session) -> User:
    """
    Fetch a user by ID from the database.
    Raises HTTPException if the user is not found or DB error occurs.
    """
    try:
        user = db.get(User, user_id)  
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        # Catch any unexpected DB errors
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

# app/services/user_service.py

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate


def update_user_service(
    user_id: int,
    user_in: UserUpdate,
    db: Session
) -> User:
    """
    Update an existing user's details.
    """
    try:
        print(user_id,user_in)
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_in.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    except HTTPException:
        # re-raise known API errors
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update user"
        )


def delete_user_service(user_id: int, db: Session) -> None:
    """
    Delete a user by ID.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    try:
        db.delete(user)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )

def get_all_users_service(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    """
    Fetch paginated list of users.
    """
    try:
        users = (
            db.query(User)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return users
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch users"
        )