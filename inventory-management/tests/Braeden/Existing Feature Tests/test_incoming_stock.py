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

    # Check the product was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Get the product id
    product = product_response.get_json()
    product_id = product["id"]

    original_quantity = product["quantity_on_hand"]

    # Create the dummy transaction
    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": 0
    }

    # Check the transaction was created
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 201

    # Get the updated product information
    updated_product_response = client.get(f"/products/{product_id}")
    updated_product = updated_product_response.get_json()

    # Check if the quantity stayed the same after adding 0
    assert updated_product["quantity_on_hand"] == original_quantity


def test_one_stock_addition(client):
    """Ensure adding one stock to a product
    does increase its quantity by 1
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 1.00,
        "quantity_on_hand": 1,
    }

    # Check if the product was made
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Get the id
    product = product_response.get_json()
    product_id = product["id"]

    original_quantity = product["quantity_on_hand"]

    # Create dummy transaction
    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": 1
    }

    # Ensure the transaction was made
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 201

    # Get the expected quantity
    transaction = transaction_response.get_json()
    additional_quantity = transaction["quantity"]
    result_quantity = additional_quantity + original_quantity

    # Get the updated product information
    updated_product_response = client.get(f"/products/{product_id}")
    updated_product = updated_product_response.get_json()

    # Check the updated quantity matches the expected one
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

    # Check if the product was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Get the product id
    product = product_response.get_json()
    product_id = product["id"]

    # Create the dummy transaction
    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": -1
    }
    

    # Ensure it failed to create (-1 is invalid)
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 400

    # Ensure the product didnt update even though the transaction failed
    updated_product_response = client.get(f"/products/{product_id}")
    updated_product = updated_product_response.get_json()
    assert updated_product["quantity_on_hand"] == 1

def test_invalid_product_id(client):
    """Ensure adding stock to a nonexistent product
    returns an error
    """

    # Create the dummy transaction
    transaction_dummy = {
        "product_id": 99999,
        "type": "IN",
        "quantity": 1
    }

    # No transaction created since product id is invalid
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

    # Ensure it was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the dummy transaction
    transaction_dummy = {
        "product_id": 1,
        "type": "IN",
        "quantity": 1,
        "supplier_id": 9999
    }

    # Ensure the transaction failed
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 404

    # Ensure the product didnt update even though the transaction failed
    updated_product_response = client.get(f"/products/{1}")
    updated_product = updated_product_response.get_json()
    assert updated_product["quantity_on_hand"] == 1