def test_product_exists_updater(client):
    """Ensure a product can be updated with new
    information
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

    # Ensure the items in product are correct
    product = product_response.get_json()
    assert product["name"] == "Dummy"
    assert product["sku"] == "DUM-001"
    assert product["unit_price"] == 1.00
    assert product["quantity_on_hand"] == 0

    # Update the product with new info
    product_id = product["id"]
    updated_dummy = client.put(f"/products/{product_id}", json={
        "name": "NewDum",
        "sku": "NEDU-111",
        "unit_price": 0.00,
        "quantity_on_hand": 1
    })

    # Ensure the update worked
    assert updated_dummy.status_code == 200

    # Ensure the new information was pushed properly
    product = updated_dummy.get_json()
    assert product["name"] == "NewDum"
    assert product["sku"] == "NEDU-111"
    assert product["unit_price"] == 0.00
    assert product["quantity_on_hand"] == 1


def test_product_no_exist_updater(client):
    """Ensure a product that does not be 
    exist cannot be updated with new information
    """ 
    # Try to update bad product
    updated_dummy = client.put(f"/products/{999}", json={
        "name": "NewDum",
        "sku": "NEDU-111",
        "unit_price": 0.00,
        "quantity_on_hand": 1
    })

    # Ensure does not exist
    assert updated_dummy.status_code == 404

