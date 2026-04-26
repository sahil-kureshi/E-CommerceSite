from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Customer Schemas ---
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class Customer(CustomerBase):
    customer_id: int
    class Config:
        from_attributes = True

class CustomerCreate(CustomerBase):
    password: str

class CustomerResponse(CustomerBase):
    customer_id: int
    class Config:
        from_attributes = True
        
class LoginRequest(BaseModel):
    email: str
    password: str
    
class CustomerUpdate(CustomerBase):
    pass

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    description: Optional[str] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int
    class Config:
        from_attributes = True

class Product(ProductBase):
    product_id: int
    class Config:
        from_attributes = True
        
class ProductUpdate(ProductBase):
    pass
        

# --- Order Schemas ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemBase]

class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    status: str
    total_amount: float
    items: List[OrderItemBase]
    class Config:
        from_attributes = True
        
class Order(OrderItemBase):
    order_id: int
    class Config:
        from_attributes = True

# --- Payment Schemas ---
class PaymentBase(BaseModel):
    order_id: int
    gateway_reference: str
    amount: float
    status: str

class PaymentResponse(PaymentBase):
    payment_id: int
    payment_date: datetime
    class Config:
        from_attributes = True
        
class Payment(PaymentBase):
    payment_id: int
    class Config:
        from_attributes = True
        
        

