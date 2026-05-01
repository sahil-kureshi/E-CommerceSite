from typing import Annotated, TypeAlias
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import models, schemas
from database import get_db
from config import settings
from starlette import status

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[str, Depends(oauth2_scheme)]

# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT helpers
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Signup
@router.post("/signup", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
def signup(customer: schemas.CustomerCreate, db: db_dependency):
    existing = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        role=customer.role,
        password=hash_password(customer.password)
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# Login
@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    customer = db.query(models.Customer).filter(models.Customer.email == form_data.username).first()
    if not customer or not verify_password(form_data.password, customer.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(customer.customer_id)})
    return {"access_token": token, "token_type": "bearer"}


def get_current_customer(token: token_dependency):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        customer_id: int = payload.get("sub")
        if customer_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return{ 'id': customer_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    # if customer is None:
    #     raise HTTPException(status_code=401, detail="User not found")
    # return customer

customer_dependency : TypeAlias = Annotated[dict, Depends(get_current_customer)]

# Get current user profile
@router.get("/me", response_model=schemas.CustomerResponse)
def get_my_profile(customer: customer_dependency, db: db_dependency):
    customer_model = db.query(models.Customer).filter(models.Customer.customer_id == customer.get('id'))\
        .first()
    if not customer_model:
        raise HTTPException(status_code=404, detail="User not found")
    return customer_model

# Update profile
@router.put("/update", response_model=schemas.CustomerResponse)
def update_profile(updated: schemas.CustomerUpdate, customer: customer_dependency, db: db_dependency):
    customer_model = db.query(models.Customer).filter(models.Customer.customer_id == customer.get('id')).first()
    if not customer_model:
        raise HTTPException(status_code=404, detail="User not found")

    customer.name = updated.name or customer_model.name
    customer.phone = updated.phone or customer_model.phone
    customer.address = updated.address or customer_model.address
    db.commit()
    db.refresh(customer)
    return customer
