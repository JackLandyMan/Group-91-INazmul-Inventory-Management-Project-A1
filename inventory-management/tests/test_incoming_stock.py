def test_zero_stock_addition(client):
    """Ensure adding zero stock to a product
    does not increase its quantity
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 1.00,
        "quantity_on_hand": 1,
    }

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

     
    product = product_response.get_json()
    product_id = product["id"]

    original_quantity = product["quantity_on_hand"]


    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": 0
    }

    transaction_response = client.post("/transactions", json=transaction_dummy)

    assert transaction_response.status_code == 201

    updated_product_response = client.get(f"/products/{product_id}")
    updated_product = updated_product_response.get_json()

    assert updated_product["quantity_on_hand"] == original_quantity


def test_one_stock_addition(client):
    """Ensure adding one stock to a product
    does increase its quantity
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 1.00,
        "quantity_on_hand": 1,
    }

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

     
    product = product_response.get_json()
    product_id = product["id"]

    original_quantity = product["quantity_on_hand"]


    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": 1
    }

    transaction_response = client.post("/transactions", json=transaction_dummy)
    transaction = transaction_response.get_json()
    additional_quantity = transaction["quantity"]

    result_quantity = additional_quantity + original_quantity

    assert transaction_response.status_code == 201

    updated_product_response = client.get(f"/products/{product_id}")
    updated_product = updated_product_response.get_json()

    assert updated_product["quantity_on_hand"] == result_quantity

def test_negative_stock_addition(client):
    """Ensure adding negative stock to a product
    results in an error
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 1.00,
        "quantity_on_hand": 1,
    }

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

     
    product = product_response.get_json()
    product_id = product["id"]

    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": -1
    }

    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 400

    updated_product_response = client.get(f"/products/{product_id}")
    updated_product = updated_product_response.get_json()
    assert updated_product["quantity_on_hand"] == 1

def test_invalid_product_id(client):
    """Ensure adding stock to a nonexistent product
    returns an error
    """

    transaction_dummy = {
        "product_id": 99999,
        "type": "IN",
        "quantity": 1
    }

    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 404

def test_invalid_supplier_id(client):
    """Ensure adding stock to a nonexistent product
    returns an error
    """

    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 1.00,
        "quantity_on_hand": 1,
    }

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    transaction_dummy = {
        "product_id": 1,
        "type": "IN",
        "quantity": 1,
        "supplier_id": 9999
    }

    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 404