def test_product_id_incorrect(client):
    """Determines whether the inputted product id exists in the system
    before attempting a transaction with it. This ensures products that
    do not exist are not entered into the system
    """
    
    #Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 100,
    }

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    #Create the dummy transaction for the dummy product
    transaction_dummy = {
        "product_id": 999,
        "type": "OUT",
        "quantity": 10,
    }

    #Confirm if successful
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 404