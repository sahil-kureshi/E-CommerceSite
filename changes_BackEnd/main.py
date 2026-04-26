from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from routers.customers import get_current_customer
from database import SessionLocal, engine
import models
<<<<<<< Updated upstream
=======
from config import settings
from routers import auth, customers, orders, payments, products
>>>>>>> Stashed changes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:5173"
]


app.add_middleware(
    
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers= ["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

<<<<<<< Updated upstream
=======

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(products.router)



'''

>>>>>>> Stashed changes
@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/orders")
def create_order(order_data: dict, db: Session = Depends(get_db)):
    # Simplified logic: validate, calculate total, create order
    new_order = models.Order(
        customer_id=order_data["customer_id"],
        status="Pending",
        total_amount=order_data["total_amount"]
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"order_id": new_order.order_id, "status": "Created"}


@app.get("/orders/me")
def get_my_orders(current_customer: models.Customer = Depends(get_current_customer), db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.customer_id == current_customer.customer_id).all()
    
    '''