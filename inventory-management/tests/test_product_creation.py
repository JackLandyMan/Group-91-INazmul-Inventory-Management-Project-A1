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

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201
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

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 201
   
    product_dummy2 = {
        "name": "Dummy",
        "sku": "DUM-001",
        "unit_price": 0.00,
        "quantity_on_hand": 0,
    }

    product_response = client.post("/products", json=product_dummy2)
    assert product_response.status_code == 201

    list_response = client.get("/products")
    assert list_response.status_code == 200

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

    product_response = client.post("/products", json=product_dummy)
    assert product_response.status_code == 400