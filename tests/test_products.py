import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a new session for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the default get_db dependency with our test version
app.dependency_overrides[get_db] = override_get_db

# Set up the test client
client = TestClient(app)

# Create the database and tables
Base.metadata.create_all(bind=engine)

# Test Product Data
test_product = {
    "name": "Test Product",
    "description": "Test Description",
    "price": 99.99
}

# Test the POST /products endpoint
def test_create_product():
    response = client.post("/products", json=test_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_product["name"]
    assert "id" in data  # Ensure the product was created with an ID

# Test the GET /products endpoint
def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test the GET /products/{id} endpoint
def test_get_product_by_id():
    # Create a product first
    response = client.post("/products", json=test_product)
    product_id = response.json()["id"]

    # Fetch the product by ID
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id

# Test the PUT /products/{id} endpoint
def test_update_product():
    # Create a product first
    response = client.post("/products", json=test_product)
    product_id = response.json()["id"]

    # Update the product
    updated_product = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 199.99
    }
    response = client.put(f"/products/{product_id}", json=updated_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"

# Test the DELETE /products/{id} endpoint
def test_delete_product():
    # Create a product first
    response = client.post("/products", json=test_product)
    product_id = response.json()["id"]

    # Delete the product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}

    # Ensure the product no longer exists
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404
