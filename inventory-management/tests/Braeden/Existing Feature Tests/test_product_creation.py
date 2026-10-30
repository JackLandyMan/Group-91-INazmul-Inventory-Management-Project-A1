def test_no_product_name(client):
    """Ensure a product can not be created
    without a name
    """

    # Create the dummy product
    product_dummy = {
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 100,
    }

    # Ensure fails with no product name
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 400

def test_no_sku(client):
    """Ensure a product can not be created
    without a sku
    """

    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "unit_price": 0.00,
        "quantity_on_hand": 100,
    }

    # Ensure fails with no sku
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 400

def test_no_quantity(client):
    """Ensure a product with no quantity
    can exist
    """

    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 0,
    }

    # Ensure product is created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Ensure the quantity is correct
    product = product_response.get_json()
    assert product["quantity_on_hand"] == 0


def test_product_dupe_name_sku(client):
    """Ensure two products with the same
    name and sku can exist at once
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 0,
    }

    # Ensure the product is created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201

    # Create the second dummy product
    product_dummy2 = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 0,
    }

    # Ensure the second product is created
    product_response = client.post("/products", json=product_dummy2)
    assert product_response.status_code == 201

    # Ensure the list exists
    list_response = client.get("/products")
    assert list_response.status_code == 200

    # Ensure all the products exist separately and are not the same
    products = list_response.get_json()
    assert len(products) == 2
    assert products[0]["name"] == "Dummy"
    assert products[1]["name"] == "Dummy"
    assert products[0] != products[1]

def test_negative_quantity(client):
    """Ensure the quantity of products cannot
    be negative
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": -1,
    }

    # Ensure product is not created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 400

def test_negative_price(client):
    """Ensure the quantity of products cannot
    be negative
    """ 
    # Create the dummy product
    product_dummy = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": -1.00,
        "quantity_on_hand": 0,
    }

    # Ensure product is not created
    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 400