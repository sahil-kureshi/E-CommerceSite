from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated, TypeAlias
import models, schemas
from database import get_db
from .auth import *

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

customer_dependency: TypeAlias = Annotated[dict, Depends(get_current_customer)]

# Create new order
@router.post("", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, customer: customer_dependency, db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    new_order = models.Order(
        customer_id=order.customer_id,
        total_amount=sum([item.price * item.quantity for item in order.items]),
        status="Pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Save order items
    for item in order.items:
        order_item = models.OrderItem(
            order_id=new_order.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(order_item)
    db.commit()

    return new_order

# Get all orders for logged-in customer
@router.get("/me", response_model=List[schemas.OrderResponse])
def get_my_orders(customer_id: int, customer: customer_dependency , db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    return orders

# Get single order by ID
@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, customer: customer_dependency , db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Update order status (Admin or system)
@router.put("/{order_id}/update_status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status: str, customer: customer_dependency, db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    db.refresh(order)
    return order

# Delete order (optional, admin only)
@router.delete("/{order_id}")
def delete_order(order_id: int, customer: customer_dependency, db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully"}