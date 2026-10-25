def test_transaction_contains_supplier_name(client):
    """Determines whether the supplier name is added to the transactions
    section of the inplemented system. It should return true if the transactions 
    dictionary for supplier name is equal to the inputed name in the dummy
    transaction
    """
    
    #Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 100,
    }

    response = client.post("/products", json=product_dummy)
    assert response.status_code == 201
    product_id = response.get_json()["id"]

    #Create the dummy supplier
    supplier_dummy = {
        "name": "Supplier",
        "contact_email": "sup@gmail.ca",
    }

    response = client.post("/suppliers", json=supplier_dummy)
    assert response.status_code == 201
    supplier_id = response.get_json()["id"]

    #Create the dummy transaction for the dummy supplier
    transaction_dummy = {
        "product_id": product_id,
        "type": "IN",
        "quantity": 10,
        "supplier_id": supplier_id
    }

    transaction_response = client.post("/transactions", json=transaction_dummy)

    assert transaction_response.status_code == 201
    transaction = transaction_response.get_json()

    #Confirm if successful
    assert transaction["supplier_name"] == "Supplier"