from unittest.mock import patch
from app import store


#Notification system testing
@patch("app.routes.transactions.send_notification", return_value=True)
def test_notification_success(mock_send, client):
    """Ensures a notification is successfully sent exactly
    once once a product stock reaches its threashhold. Also 
    ensures the API returns true on success. 
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 6,
    }

    # Ensure the product was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the dummy product
    supplier_dummy = {
        "name": "DummyS",
        "contact_email": "a@a.ca",
    }

    # Ensure the product was created
    supplier_response = client.post("/suppliers", json=supplier_dummy)
    assert supplier_response.status_code == 201
    

    # Create the dummy transaction
    transaction_dummy = {
        "product_id": 1,
        "supplier_id": 1,
        "type": "OUT",
        "quantity": 2,
    }
    
    # Ensure the transaction was created
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 201

    # Ensure the API returns true
    assert transaction_response.json["notification_sent"] is True

    # Ensure the notification was sent exactly once
    mock_send.assert_called_once()


@patch("app.routes.transactions.send_notification", return_value=True)
def test_notification_correct(mock_send, client):
    """Ensures the notification is sent to the correct recipiant
    and has the correct subject and message. Also ensures the API 
    returns true on success. 
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 6,
    }

    # Ensure the product was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the dummy product
    supplier_dummy = {
        "name": "DummyS",
        "contact_email": "a@a.ca",
    }

    # Ensure the product was created
    supplier_response = client.post("/suppliers", json=supplier_dummy)
    assert supplier_response.status_code == 201
    

    # Create the dummy transaction
    transaction_dummy = {
        "product_id": 1,
        "supplier_id": 1,
        "type": "OUT",
        "quantity": 2,
    }
    
    # Ensure the transaction was created
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 201

    # Ensure the API returns true
    assert transaction_response.json["notification_sent"] is True

    # Ensure the correct notification was sent
    mock_send.assert_called_once_with("a@a.ca", "Low Stock Alert!", f"Hello DummyS, \nDummy has 4 units remaining. \nPlease arrange to restock this product.")


@patch("app.routes.transactions.send_notification", return_value=True)
def test_transaction_completes_with_notification(mock_send, client):
    """Ensures the transaction is properly saved and the quantity
    of the products stock updates appropriately. Also ensures the
    API returns true"""

    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 6,
    }

    # Ensure the product was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the dummy product
    supplier_dummy = {
        "name": "DummyS",
        "contact_email": "a@a.ca",
    }

    # Ensure the product was created
    supplier_response = client.post("/suppliers", json=supplier_dummy)
    assert supplier_response.status_code == 201
    

    # Create the dummy transaction
    transaction_dummy = {
        "product_id": 1,
        "supplier_id": 1,
        "type": "OUT",
        "quantity": 2,
    }
    
    # Ensure the transaction was created
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 201

    # Ensure the API returns true
    assert transaction_response.json["notification_sent"] is True

    # Ensure the product quantity updated
    product_id = product_response.json["id"]
    assert store.products[product_id].quantity_on_hand == 4

    # Ensure the transaction actually made it to the list
    assert transaction_response.json["id"] in store.transactions

    # Ensure the notification was sent exactly once
    mock_send.assert_called_once()

#Purchase order testing
def test_create_product(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    response = client.post("/products", json=product_dummy)

    #Ensure its created
    assert response.status_code == 201
    # return response.json["id"]

def test_create_supplier(client):
    supplier_dummy = {
        "name": "Dummy",
        "contact_email": "dum@dum.ca",
    }
    response = client.post("/suppliers", json=supplier_dummy)

    #Ensure its created
    assert response.status_code == 201
    # return response.json["id"]


def test_create_purchase_order(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

    supplier_dummy = {
        "name": "Dummy",
        "contact_email": "dum@dum.ca",
    }
    supplier_response = client.post("/suppliers", json=supplier_dummy)

    #Ensure the supplier is created
    assert supplier_response.status_code == 201

    response = client.post("/purchase-orders", json={
        "product_id": product_response.get_json()["id"],
        "supplier_id": supplier_response.get_json()["id"],
        "quantity_ordered": 10,
    })

    #Ensure the order response is created
    assert response.status_code == 201
    assert response.json["status"] == "pending"
    assert response.json["product_id"] == product_response.get_json()["id"]
    assert response.json["supplier_id"] == supplier_response.get_json()["id"]


def test_list_product_order(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

    supplier_dummy = {
        "name": "Dummy",
        "contact_email": "dum@dum.ca",
    }
    supplier_response = client.post("/suppliers", json=supplier_dummy)

    #Ensure the supplier is created
    assert supplier_response.status_code == 201

    order_response = client.post("/purchase-orders", json={
        "product_id": product_response.get_json()["id"],
        "supplier_id": supplier_response.get_json()["id"],
        "quantity_ordered": 10,
    })

    #Ensure the product response is created
    assert order_response.status_code == 201


    response = client.get("/purchase-orders")
    #Ensure the list exists
    assert response.status_code == 200


def test_supplier_false_order(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

    response = client.post("/purchase-orders", json={
        "product_id": product_response.get_json()["id"],
        "supplier_id": 9999,
        "quantity_ordered": 10,
    })

    #Ensure the order does not exist (due to supplier)
    assert response.status_code == 404
    assert response.json["error"] == "Supplier not found"


def test_product_false_order(client):
    supplier_dummy = {
        "name": "Dummy",
        "contact_email": "dum@dum.ca",
    }
    supplier_response = client.post("/suppliers", json=supplier_dummy)

    #Ensure the supplier is created
    assert supplier_response.status_code == 201

    response = client.post("/purchase-orders", json={
        "product_id": 9999,
        "supplier_id": supplier_response.get_json()["id"],
        "quantity_ordered": 10,
    })

    #Ensure the order does not exist (due to product)
    assert response.status_code == 404
    assert response.json["error"] == "Product not found"


def test_purchase_false(client):
    response = client.get("/purchase-orders/9999")

    #Ensure does not exist
    assert response.status_code == 404
    assert response.json["error"] == "Purchase order not found"

def test_purchase_receive(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

    supplier_dummy = {
        "name": "Dummy",
        "contact_email": "dum@dum.ca",
    }
    supplier_response = client.post("/suppliers", json=supplier_dummy)

    #Ensure the supplier is created
    assert supplier_response.status_code == 201

    order_response = client.post("/purchase-orders", json={
        "product_id": product_response.get_json()["id"],
        "supplier_id": supplier_response.get_json()["id"],
        "quantity_ordered": 10,
    })

    #Ensure the product response is created
    assert order_response.status_code == 201

    response = client.put(f"/purchase-orders/{order_response.get_json()["id"]}/receive")

    #Ensure receive exists
    assert response.status_code == 200
    assert response.json["status"] == "received"

def test_purchase_receive_false(client):
    response = client.put("/purchase-orders/9999/receive")

    #Ensure it does not exist
    assert response.status_code == 404
    assert response.json["error"] == "Purchase order not found"

#Products testing
def test_create_product(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

def test_low_stock(client):
    low_product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 2,
    }
    product_response = client.post("/products", json=low_product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

    high_product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 20,
    }
    product_response = client.post("/products", json=high_product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

    response = client.get("/products/low-stock")

    #Ensure low stock exists
    assert response.status_code == 200

def test_get_product(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)

    #Ensure the product is created
    assert product_response.status_code == 201

    response = client.get(f"/products/{product_response.get_json()["id"]}")    

    #Ensure it exists
    assert response.status_code == 200
    assert response.json["id"] == product_response.get_json()["id"]
    assert response.json["name"] == "Dummy"

def test_product_false(client):
    response = client.get("/products/9999")

    #Ensure does not exist
    assert response.status_code == 404
    assert response.json["error"] == "Product not found"


def test_stock_level(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)
   
    #Ensure the product is created
    assert product_response.status_code == 201

    response = client.get(f"/products/{product_response.get_json()["id"]}/stock-level")

    #Ensure its created
    assert response.status_code == 200
    assert response.json["product_id"] == product_response.get_json()["id"]
    assert response.json["quantity_on_hand"] == 5

def test_stock_level_false(client):
    response = client.get("/products/9999/stock-level")

    #Ensure fails
    assert response.status_code == 404
    assert response.json["error"] == "Product not found"


#Views testing
def test_home(client):
    response = client.get("/")

    #Ensure it exists
    assert response.status_code == 200

def test_products_page_get(client):
    response = client.get("/ui/products")

    #Ensure it exists
    assert response.status_code == 200

def test_products_post(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)
    
    #Ensure the product is created
    assert product_response.status_code == 201

    response = client.post("/ui/products", data=product_dummy)

    #Ensure redirect
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/ui/products")

def test_delete_products_page(client):
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 10.00,
        "quantity_on_hand": 5,
    }
    product_response = client.post("/products", json=product_dummy)
    
    #Ensure the product is created
    assert product_response.status_code == 201

    response = client.post(f"/ui/products/{product_response.get_json()["id"]}/delete")

    #Ensure redirect
    assert response.status_code == 302

def test_delete_products_page_false(client):
    response = client.post("/ui/products/9999/delete")

    #Ensure redirect
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/ui/products")