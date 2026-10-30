def test_product_exists_one_delete(client):
    """Ensure one product can be deleted when one
    is existing
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 1.00,
        "quantity_on_hand": 0,
    }

    # Check if it was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Get a list of all products and ensure it was got
    list_response = client.get("/products")
    assert list_response.status_code == 200
    # Ensure the list length is 1
    products = list_response.get_json()
    assert len(products) == 1

    # Get id of the product
    product = product_response.get_json()
    product_id = product["id"]

    # Ensure the list is empty
    response = client.delete(f"/products/{product_id}")    
    assert response.status_code == 204
    # Ensure the list still exists
    list_response = client.get("/products")
    assert list_response.status_code == 200

    # Ensure the products length is 0
    products = list_response.get_json()
    assert len(products) == 0

def test_product_exists_two_delete(client):
    """Ensure a product can be deleted when multiple
    are existing
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 1.00,
        "quantity_on_hand": 0,
    }

    # Ensure the product was created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the dummy product
    product_dummy2 = {
        "name": "Dummy2",
        "sku": "DUM-002",
        "unit_price": 1.00,
        "quantity_on_hand": 0,
    }

    # Ensure the product was created
    product_response = client.post("/products", json=product_dummy2)
    assert product_response.status_code == 201

    # Ensure the list exists and is len 2 (for 2 products)
    list_response = client.get("/products")
    assert list_response.status_code == 200
    products = list_response.get_json()
    assert len(products) == 2

    # Delete the first item in the list
    product_id = products[0]["id"]

    # Ensure it was deleted
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    # Ensure the list exists still
    list_response = client.get("/products")
    assert list_response.status_code == 200

    # Update the product list and check the length is stil l1
    products = list_response.get_json()
    assert len(products) == 1

    # Ensure the correct product was deleted
    assert products[0]["name"] == "Dummy2"
    assert products[0]["sku"] == "DUM-002"

def test_product_no_existing_delete(client):
    """Ensure a product can not be deleted
    when it does not exist
    """ 

    # Delete a product that doesnt exist (throw error)
    response = client.delete(f"/products/{999}")
    assert response.status_code == 404

    # Ensure the list exists
    list_response = client.get("/products")
    assert list_response.status_code == 200

    # Ensure the list is 0
    products = list_response.get_json()
    assert len(products) == 0