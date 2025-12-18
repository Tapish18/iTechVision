from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Order
from app.models import Product
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse
)
from app.models import User

from app.services.order import (
    create_order_service,
    get_order_service,
    update_order_service,
    delete_order_service
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    try:
        return create_order_service(order_in, db)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while creating order"
        )



@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return get_order_service(order_id, db)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while fetching order"
        )

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_in: OrderUpdate, db: Session = Depends(get_db)):
    try:
        return update_order_service(order_id, order_in, db)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while updating order"
        )


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        delete_order_service(order_id, db)
        return {"detail": "Order deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while deleting order"
        )