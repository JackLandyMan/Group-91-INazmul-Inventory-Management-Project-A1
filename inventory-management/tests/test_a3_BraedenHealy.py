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