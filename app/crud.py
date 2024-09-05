from sqlalchemy.orm import Session
from .models import Product

def get_products(db: Session):
    return db.query(Product).all()

def get_product(db: Session, id: int):
    return db.query(Product).filter(Product.id == id).first()

def create_product(db: Session, product_data):
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def update_product(db: Session, id: int, product_data):
    product = db.query(Product).filter(Product.id == id).first()
    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    return None

def delete_product(db: Session, id: int):
    product = db.query(Product).filter(Product.id == id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False
