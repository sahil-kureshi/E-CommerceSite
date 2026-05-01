from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated, TypeAlias
import models, schemas
from .auth import *
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

customer_dependency: TypeAlias = Annotated[dict, Depends(get_current_customer)]

# Get all products
@router.get("/", response_model=List[schemas.Product])
def get_products(db: db_dependency, customer: customer_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    products = db.query(models.Product).all()
    return products

# Get product by ID
@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Add new product (Admin only)
@router.post("/", response_model=schemas.Product)
def add_product(product: schemas.ProductCreate, customer: customer_dependency, db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    new_product = models.Product(
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock,
        description=product.description,
        image_url=product.image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Update product
@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int,  updated_product: schemas.ProductUpdate, 
                   customer: customer_dependency, db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_product.name or product.name
    product.category = updated_product.category or product.category
    product.price = updated_product.price or product.price
    product.stock = updated_product.stock or product.stock
    product.description = updated_product.description or product.description
    product.image_url = updated_product.image_url or product.image_url

    db.commit()
    db.refresh(product)
    return product

# Delete product
@router.delete("/{product_id}")
def delete_product(product_id: int, customer: customer_dependency, db: db_dependency):
    if customer is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": f"Product {product_id} deleted successfully"}