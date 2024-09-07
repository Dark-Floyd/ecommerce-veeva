from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

# Create a new session for testing
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


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
    assert "id" in data

# Test the GET /products endpoint
def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test the GET /products/{id} endpoint
def test_get_product_by_id():
    response = client.post("/products", json=test_product)
    product_id = response.json()["id"]

    # Fetch the product by ID
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id

# Test the PUT /products/{id} endpoint
def test_update_product():
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
    response = client.post("/products", json=test_product)
    product_id = response.json()["id"]

    # Delete the product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}

    # Ensure the product no longer exists
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404

# Test for missing fields
def test_create_product_missing_field():
    # Test missing name field
    response = client.post(
        "/products", json={"description": "Test Description", "price": 99.99})
    # Unprocessable Entity (validation error)
    assert response.status_code == 422

# Test invalid data types
def test_create_product_invalid_data_type():
    # Price as a string instead of a float
    response = client.post(
        "/products", json={"name": "Test", "description": "Invalid price", "price": "abc"})
    assert response.status_code == 422

# Test for non-existent product retrieval
def test_get_nonexistent_product():
    response = client.get("/products/999")  # Assuming 999 doesn't exist
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

# Test for updating a non-existent product
def test_update_nonexistent_product():
    # Assuming 999 doesn't exist
    response = client.put("/products/999", json=test_product)
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

# Test for deleting a non-existent product
def test_delete_nonexistent_product():
    response = client.delete("/products/999")  # Assuming 999 doesn't exist
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
