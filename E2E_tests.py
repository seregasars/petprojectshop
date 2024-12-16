import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:5000"

def test_user_authorization_and_order_creation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Add User
        page.goto(f"{BASE_URL}/add_user_form")
        page.wait_for_selector("input#username")  # Ждем, пока элемент не станет доступен
        page.fill("input#username", "test_user")
        page.click("button[type='submit']")
        assert "User test_user added successfully!" in page.content()

        # 2. Add Product
        response = page.request.post(
            f"{BASE_URL}/add_product",
            data={"name": "Laptop", "price": 1000, "stock": 10},
        )
        assert response.status == 201
        assert response.json()["message"] == "Product Laptop added"

        # 3. Create Order
        response = page.request.post(
            f"{BASE_URL}/create_order",
            data={"username": "test_user", "product_name": "Laptop", "quantity": 2},
        )
        assert response.status == 201
        assert response.json()["message"] == "Order created for test_user"

        browser.close()

def test_sales_report_and_error_handling():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Add User
        response = page.request.post(
            f"{BASE_URL}/add_user",
            data={"username": "test_user"},
        )
        assert response.status == 201

        # 2. Add Product
        response = page.request.post(
            f"{BASE_URL}/add_product",
            data={"name": "Smartphone", "price": 500, "stock": 5},
        )
        assert response.status == 201

        # 3. Create Order
        response = page.request.post(
            f"{BASE_URL}/create_order",
            data={"username": "test_user", "product_name": "Smartphone", "quantity": 2},
        )
        assert response.status == 201

        # 4. Get Sales Report
        response = page.request.get(f"{BASE_URL}/get_sales_report")
        assert response.status == 200
        assert "Smartphone - Sold: 2, Remaining Stock: 3" in response.json()["report"]

        # Error Handling: Order more than stock
        response = page.request.post(
            f"{BASE_URL}/create_order",
            data={"username": "test_user", "product_name": "Smartphone", "quantity": 10},
        )
        assert response.status == 400
        assert response.json()["error"] == "Not enough stock to fulfill order"

        # Error Handling: User not found
        response = page.request.post(
            f"{BASE_URL}/create_order",
            data={"username": "unknown_user", "product_name": "Smartphone", "quantity": 1},
        )
        assert response.status == 400
        assert response.json()["error"] == "User not found"

        # Error Handling: Product not found
        response = page.request.post(
            f"{BASE_URL}/create_order",
            data={"username": "test_user", "product_name": "Unknown Product", "quantity": 1},
        )
        assert response.status == 400
        assert response.json()["error"] == "Product not found"

        browser.close()
