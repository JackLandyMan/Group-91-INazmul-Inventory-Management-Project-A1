def test_transaction_contains_product_name(client):
    """Determines whether the product name is added to the transactions 
    section of the inplemented system. It should return true if the transactions 
    dictionary for product name is equal to the inputed name in the dummy
    transaction
    """
    
    #Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 100,
    }

    # Ensure the product was created
    response = client.post("/products", json=product_dummy)
    assert response.status_code == 201

    product_id = response.get_json()["id"]

    # Create the dummy transaction for the dummy product
    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": 10,
    }

    # Ensure the transaction was created
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 201

    # Ensure the product name is correct 
    transaction = transaction_response.get_json()
    assert transaction["product_name"] == "Dummy"