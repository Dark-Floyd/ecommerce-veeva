from fastapi import FastAPI, HTTPException
from .schemas import Product, ProductCreate
from .crud import get_product, create_product, update_product, delete_product, get_products
from .routes import router as product_router
from .database import Base, engine

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# Create the FastAPI instance
app = FastAPI()

# Include the product router
app.include_router(product_router)


@app.get("/products", response_model=list[Product])
async def list_products():
    return get_products()

@app.get("/products/{id}", response_model=Product)
async def get_product_by_id(id: int):
    product = get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product)
async def create_new_product(product: ProductCreate):
    return create_product(product)

@app.put("/products/{id}", response_model=Product)
async def update_existing_product(id: int, product: ProductCreate):
    updated_product = update_product(id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/{id}", response_model=dict)
async def delete_existing_product(id: int):
    success = delete_product(id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
