def test_empty_product_list(client):
    """Checks an empty product list returns the correct code
    when empty
    """
    
    product_response = client.get("/products")
    assert product_response.status_code == 200
    assert product_response.get_json() == []

def test_single_product_list(client):
    """Determines whether a single product is
    returned properly when checked
    """

    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 100,
    }

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Get the product list
    list_response = client.get("/products")
    assert list_response.status_code == 200

    # Check that the list contains one product
    products = list_response.get_json()
    assert len(products) == 1
    assert products[0]["name"] == "Dummy"
    assert products[0]["sku"] == "DUM-001"


def test_double_product_list(client):
    """Determines whether a multiple products are
    returned properly when checked
    """

    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 100,
    }

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the dummy product
    product_dummy2 = {
        "name": "Dummy2",
        "sku": "DUM-002",
        "unit_price": 1.00,
        "quantity_on_hand": 1,
    }

    product_response = client.post("/products", json=product_dummy2)
    assert product_response.status_code == 201

    # Get the product list
    list_response = client.get("/products")
    assert list_response.status_code == 200

    # Check that the list contains one product
    products = list_response.get_json()
    assert len(products) == 2
    assert products[0]["name"] == "Dummy"
    assert products[0]["sku"] == "DUM-001"
    assert products[1]["name"] == "Dummy2"
    assert products[1]["sku"] == "DUM-002"