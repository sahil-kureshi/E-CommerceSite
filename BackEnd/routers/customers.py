from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .auth import *
import models
from database import get_db

router = APIRouter()

@router.post("/signup")
def signup(name: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.Customer).filter(models.Customer.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(password)
    new_customer = models.Customer(name=name, email=email, hashed_password=hashed_pw)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Signup successful", "customer_id": new_customer.customer_id}



@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Customer).filter(models.Customer.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.Customer).filter(models.Customer.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

