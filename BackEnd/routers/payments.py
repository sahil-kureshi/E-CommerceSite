from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, TypeAlias
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import razorpay
import os
from dotenv import load_dotenv
from .auth import *

customer_dependency: TypeAlias = Annotated[dict, Depends(get_current_customer)]

load_dotenv()

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))

@router.post("/create-payment")
def create_payment(order_id: int, customer: customer_dependency , db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # Fetch order details
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create({
        "amount": int(order.total_amount * 100),  # amount in Paise
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save payment record in DB
    payment = models.Payment(
        order_id=order.order_id,
        gateway_reference=razorpay_order["id"],
        amount=order.total_amount,
        status="Created"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {"razorpay_order_id": razorpay_order["id"], "amount": order.total_amount}

@router.post("/verify-payment")
def verify_payment(payment_id: str, razorpay_payment_id: str, razorpay_signature: str,
                   customer: customer_dependency , db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # Verify signature
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": payment_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })
    except:
        raise HTTPException(status_code=400, detail="Payment verification failed")

    # Update payment status
    payment = db.query(models.Payment).filter(models.Payment.gateway_reference == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    payment.status = "Success"
    db.commit()

    # Update order status
    order = db.query(models.Order).filter(models.Order.order_id == payment.order_id).first()
    order.status = "Paid"
    db.commit()

    return {"message": "Payment verified successfully", "order_id": order.order_id}