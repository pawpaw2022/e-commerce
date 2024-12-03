import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from app.main import app

client = TestClient(app)

# Mock data for testing
mock_category = {
    "categoryName": "Test Category"
}

mock_product = {
    "productName": "Test Product",
    "categoryId": 1,
    "price": "19.99"
}

mock_customer = {
    "firstName": "John",
    "lastName": "Doe",
    "addressState": "CA"
}

mock_order = {
    "customerId": 1,
    "productId": 1,
    "quantity": 2
}

mock_review = {
    "customerId": 1,
    "productId": 1,
    "rating": 8
}

# Category Tests
def test_create_category():
    response = client.post("/categories/", json=mock_category)
    assert response.status_code == 201
    data = response.json()
    assert "category" in data
    assert data["category"]["categoryName"] == mock_category["categoryName"]

def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert isinstance(data["categories"], list)

def test_get_category():
    # First create a category
    create_response = client.post("/categories/", json=mock_category)
    category_id = create_response.json()["category"]["categoryId"]
    
    # Then get it
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["categoryName"] == mock_category["categoryName"]

def test_delete_category():
    # First create a category
    create_response = client.post("/categories/", json=mock_category)
    category_id = create_response.json()["category"]["categoryId"]
    
    # Then delete it
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["category_id"] == category_id

# Product Tests
def test_create_product():
    response = client.post("/products/", json=mock_product)
    assert response.status_code == 201
    data = response.json()
    assert "product" in data
    assert data["product"]["productName"] == mock_product["productName"]

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)

def test_get_product():
    # First create a product
    create_response = client.post("/products/", json=mock_product)
    product_id = create_response.json()["product"]["productId"]
    
    # Then get it
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["productName"] == mock_product["productName"]

def test_delete_product():
    # First create a product
    create_response = client.post("/products/", json=mock_product)
    product_id = create_response.json()["product"]["productId"]
    
    # Then delete it
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["product_id"] == product_id

# Customer Tests
def test_create_customer():
    response = client.post("/customers/", json=mock_customer)
    assert response.status_code == 201
    data = response.json()
    assert "customer" in data
    assert data["customer"]["firstName"] == mock_customer["firstName"]

def test_get_customers():
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert "customers" in data
    assert isinstance(data["customers"], list)

def test_update_customer():
    # First create a customer
    create_response = client.post("/customers/", json=mock_customer)
    customer_id = create_response.json()["customer"]["customerId"]
    
    # Update the customer
    update_data = {"firstName": "Jane"}
    response = client.patch(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["customer"]["firstName"] == "Jane"

def test_delete_customer():
    # First create a customer
    create_response = client.post("/customers/", json=mock_customer)
    customer_id = create_response.json()["customer"]["customerId"]
    
    # Then delete it
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.json()["customer_id"] == customer_id

# Order Tests
def test_create_order():
    response = client.post("/orders/", json=mock_order)
    assert response.status_code == 201
    data = response.json()
    assert "order" in data
    assert data["order"]["quantity"] == mock_order["quantity"]

def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert "orders" in data
    assert isinstance(data["orders"], list)

def test_delete_order():
    # First create an order
    create_response = client.post("/orders/", json=mock_order)
    order_id = create_response.json()["order"]["orderId"]
    
    # Then delete it
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["order_id"] == order_id

# Review Tests
def test_create_review():
    response = client.post("/reviews/", json=mock_review)
    assert response.status_code == 201
    data = response.json()
    assert "review" in data
    assert data["review"]["rating"] == mock_review["rating"]

def test_get_reviews():
    response = client.get("/reviews/")
    assert response.status_code == 200
    data = response.json()
    assert "reviews" in data
    assert isinstance(data["reviews"], list)

def test_delete_review():
    # First create a review
    create_response = client.post("/reviews/", json=mock_review)
    review_id = create_response.json()["review"]["reviewId"]
    
    # Then delete it
    response = client.delete(f"/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json()["review_id"] == review_id 