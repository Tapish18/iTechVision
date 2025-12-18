from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Order
from app.models import Product
from app.models import User
from app.schemas.order import OrderCreate, OrderUpdate
from enum import Enum

# Define allowed statuses
class OrderStatusEnum(str, Enum):
    CREATED = "CREATED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

def create_order_service(order_in: OrderCreate, db: Session) -> Order:
    # Validate user
    user = db.get(User, order_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate product and stock
    product = db.get(Product, order_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < order_in.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Reduce stock
    product.stock -= order_in.quantity

    order = Order(
        user_id=order_in.user_id,
        product_id=order_in.product_id,
        quantity=order_in.quantity,
        status="CREATED"
    )
    db.add(order)

    try:
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        # Restore stock in case of failure
        product.stock += order_in.quantity
        raise HTTPException(status_code=400, detail=f"Failed to create order: {str(e)}")


def get_order_service(order_id: int, db: Session) -> Order:
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# def update_order_service(order_id: int, order_in: OrderUpdate, db: Session) -> Order:
#     order = db.get(Order, order_id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     # If quantity changes, adjust stock
#     if order_in.quantity is not None and order_in.quantity != order.quantity:
#         product = order.product
#         diff = order_in.quantity - order.quantity
#         if diff > 0 and product.stock < diff:
#             raise HTTPException(status_code=400, detail="Insufficient stock for update")
#         product.stock -= diff
#         order.quantity = order_in.quantity

#     if order_in.status is not None:
#         # If canceling order, restore stock
#         if order_in.status.lower() == "canceled" and order.status != "CANCELED":
#             order.product.stock += order.quantity
#         order.status = order_in.status

#     try:
#         db.commit()
#         db.refresh(order)
#         return order
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=f"Failed to update order: {str(e)}")

def update_order_service(order_id: int, order_in: OrderUpdate, db: Session) -> Order:
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # If quantity changes, adjust stock
    if getattr(order_in, "quantity", None) is not None and order_in.quantity != order.quantity:
        product = order.product
        diff = order_in.quantity - order.quantity
        if diff > 0 and product.stock < diff:
            raise HTTPException(status_code=400, detail="Insufficient stock for update")
        product.stock -= diff
        order.quantity = order_in.quantity
    
    
    if getattr(order_in, "status", None) is not None:
        # Normalize status to uppercase
        new_status = order_in.status.upper()

        # Validate against allowed statuses
        if new_status not in OrderStatusEnum.__members__:
            raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {list(OrderStatusEnum.__members__.keys())}")

        # Handle cancel logic
        if new_status == "CANCELLED" and order.status not in ("CANCELLED", "DELIVERED"):
            order.product.stock += order.quantity

        order.status = new_status

    try:
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update order: {str(e)}")


def delete_order_service(order_id: int, db: Session):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Restore stock before deletion if status is either Created or Shipped
    if(order.status == "CREATED" or order.status == "SHIPPED" ):
        order.product.stock += order.quantity
    else:
        print("Stock will be restocked after returning")

    try:
        db.delete(order)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete order: {str(e)}")
