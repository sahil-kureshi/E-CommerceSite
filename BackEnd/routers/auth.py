from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import models, schemas
from database import get_db
from config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT helpers
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Signup
@router.post("/signup", response_model=schemas.Customer)
def signup(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        password=hash_password(customer.password)
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# Login
@router.post("/login")
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.email == credentials.email).first()
    if not customer or not verify_password(credentials.password, customer.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(customer.customer_id)})
    return {"access_token": token, "token_type": "bearer"}

# Get current user profile
@router.get("/me", response_model=schemas.Customer)
def get_my_profile(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    customer_id = int(payload.get("sub"))
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    return customer

# Update profile
@router.put("/me", response_model=schemas.Customer)
def update_profile(token: str, updated: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    customer_id = int(payload.get("sub"))
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")

    customer.name = updated.name or customer.name
    customer.phone = updated.phone or customer.phone
    customer.address = updated.address or customer.address
    db.commit()
    db.refresh(customer)
    return customer
