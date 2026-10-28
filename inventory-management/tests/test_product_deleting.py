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

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    list_response = client.get("/products")
    assert list_response.status_code == 200
    products = list_response.get_json()
    assert len(products) == 1
    
    product = product_response.get_json()
    product_id = product["id"]

    response = client.delete(f"/products/{product_id}")
    
    assert response.status_code == 204
    list_response = client.get("/products")
    assert list_response.status_code == 200

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

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the dummy product
    product_dummy2 = {
        "name": "Dummy2",
        "sku": "DUM-002",
        "unit_price": 1.00,
        "quantity_on_hand": 0,
    }

    product_response = client.post("/products", json=product_dummy2)
    assert product_response.status_code == 201

    list_response = client.get("/products")
    assert list_response.status_code == 200
    products = list_response.get_json()
    assert len(products) == 2

    product_id = products[0]["id"]
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    list_response = client.get("/products")
    assert list_response.status_code == 200

    products = list_response.get_json()
    assert len(products) == 1
    assert products[0]["name"] == "Dummy2"
    assert products[0]["sku"] == "DUM-002"

def test_product_no_existing_delete(client):
    """Ensure a product can not be deleted
    when it does not exist
    """ 
    response = client.delete(f"/products/{999}")
    assert response.status_code == 404

    list_response = client.get("/products")
    assert list_response.status_code == 200

    products = list_response.get_json()
    assert len(products) == 0