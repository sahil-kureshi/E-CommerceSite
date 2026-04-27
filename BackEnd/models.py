from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(15))
    address = Column(Text)
    password = Column(String(255))
    #role = Column(String)
    #is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    category = Column(String(50))
    price = Column(DECIMAL(10, 2))
    stock = Column(Integer)
    description = Column(Text)
    image_url = Column(String(255))

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    order_date = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(String(20))
    total_amount = Column(DECIMAL(10, 2))
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    gateway_reference = Column(String(100))
    amount = Column(DECIMAL(10, 2))
    status = Column(String(20))
    payment_date = Column(DateTime, default=datetime.now(timezone.utc))
    order = relationship("Order", back_populates="payment")