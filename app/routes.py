from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db

router = APIRouter()

@router.get("/products", response_model=list[schemas.Product])
async def list_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return [schemas.Product.model_construct(**product.__dict__) for product in products]  

@router.get("/products/{id}", response_model=schemas.Product)
async def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.Product.model_construct(**product.__dict__)  

@router.post("/products", response_model=schemas.Product)
async def create_new_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = crud.create_product(db, product)
    return schemas.Product.model_construct(**new_product.__dict__) 

@router.put("/products/{id}", response_model=schemas.Product)
async def update_existing_product(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    updated_product = crud.update_product(db, id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.Product.model_construct(**updated_product.__dict__) 

@router.delete("/products/{id}", response_model=dict)
async def delete_existing_product(id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
