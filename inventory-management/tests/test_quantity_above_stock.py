def test_transaction_quantity_above_stock(client):
    """Determines whether the quantity requested to be removed
    from the stock is more than the stock number. This ensures
    that the stock can never be negative after an out transaction
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

    product_id = product_response.get_json()["id"]

    #Create the dummy transaction for the dummy product
    transaction_dummy = {
        "product_id": product_id,
        "type": "OUT",
        "quantity": 10,
    }

    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 201

    #Check the quantity (should be positive)
    product_response2 = client.get(f"/products/{product_id}")
    assert product_response2.status_code == 200
    #Should be 90 cause 100-10
    assert product_response2.get_json()["quantity_on_hand"] == 90

    #Create the negative test dummy transaction for the dummy product
    transaction_dummy = {
        "product_id": product_id,
        "type": "OUT",
        "quantity": 1000,
    }
    
    transaction_response = client.post("/transactions", json=transaction_dummy)
    assert transaction_response.status_code == 400
    

    #Confirm if successful
    product_response3 = client.get(f"/products/{product_id}")
    assert product_response3.status_code == 200
    #Should still be 90 since the case got thrown out
    assert product_response3.get_json()["quantity_on_hand"] == 90