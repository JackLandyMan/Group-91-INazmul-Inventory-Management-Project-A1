from unittest.mock import patch
from app import store
from app.models.purchase_order import PurchaseOrder
from datetime import date
#Assignment 3 tests Scott Woods
#trying to trigger gitup. 
#trying to triiger gitup2

#testing the failures of the notification system
def test_notification_failure(monkeypatch, client):
    with patch("app.routes.transactions.send_notification", return_value=False) as mock_send:
        
        #make test data
        product = {
            "name": "test",
            "sku": "test1",
            "unit_price": 1.00,
            "quantity_on_hand": 6,
        }
    #check it was created
        product_response = client.post("/products", json=product)
        assert product_response.status_code == 201
    
        # Create the test product
        supplier = {
            "name": "fakeSupplier",
            "contact_email": "test@test.com",
        }
        #check it was created 
        supplier_response = client.post("/suppliers", json=supplier)
        assert supplier_response.status_code == 201
        
        #make a good transaction, see what happens is not called
        transactionOne = {
            "product_id": 1,
            "supplier_id": 1,
            "type": "OUT",
            "quantity": 1,
        }

        transaction_response = client.post("/transactions", json=transactionOne)
        #Test the notification
        #does the transaction complete? Yes
        assert transaction_response.status_code == 201
        #did notification fail? Yes
        assert transaction_response.get_json()["notification_sent"] == False
        #did it get called? No
        mock_send.assert_not_called
        #did it take away the product? Yes
        product_id = product_response.json["id"]
        assert store.products[product_id].quantity_on_hand == 5
        
        
        #set product back to 10 for testing
        store.products[product_id].quantity_on_hand = 10
        
        
        #See what happens when the notification is triggered and fails
        transactionFour = {
                "product_id": 1,
                "supplier_id": 1,
                "type": "OUT",
                "quantity": 9,
                }

        transaction_response = client.post("/transactions", json=transactionFour)
                #Test the notification
                #does the transaction complete? Yes
        assert transaction_response.status_code == 201
        #did notification fail? Yes
        assert transaction_response.get_json()["notification_sent"] == False
        #did it get called Yes
        mock_send.assert_called_once()
        #did it take away the product? Yes
        product_id = product_response.json["id"]
        assert store.products[product_id].quantity_on_hand == 1


        #these are filling up the coverage for the transaction file now. 
        #These are unrelated to the notification testing
        #sale more then on hand
        transactionTwo= {
            "product_id": 1,
            "supplier_id": 1,
            "type": "SALE",
            "quantity": 12,
        }
        

        transaction_response = client.post("/transactions", json=transactionTwo)
        assert transaction_response.status_code == 400
        assert transaction_response.get_json()["error"] == "bad value request"


        transactionThree = {
            "product_id": 1,
            "supplier_id": 1,
            "type": "OUT",
            "quantity": 7,
        }
        
        transaction_response = client.post("/transactions", json=transactionThree)
        assert transaction_response.status_code == 400 
        assert transaction_response.get_json()["error"] == "bad value request"


     #   transactionFive = {
     #       "product_id": 1,
     #       "supplier_id": 1,
     #       "type": "IN",
     #       "quantity": 17,
     #   }
        
     #   transaction_response = client.post("/transactions", json=transactionFive)
     #   assert transaction_response.status_code == 400 
     #   assert transaction_response.get_json()["error"] == "bad value request"
       

def test_list_transactions(client):
#testing to see if the array is empty.
    response = client.get("/transactions")

    assert response.status_code == 200
    assert response.get_json() == []

#testing one transaction
#make some test data
        #make test data
    product = {
            "name": "test",
            "sku": "test1",
            "unit_price": 1.00,
            "quantity_on_hand": 6,
        }
    #check it was created
    product_response = client.post("/products", json=product)
    assert product_response.status_code == 201
    
    # Create a test supplier
    supplier = {
            "name": "fakeSupplier",
            "contact_email": "test@test.com",
        }
    #check it was created 
    supplier_response = client.post("/suppliers", json=supplier)
    assert supplier_response.status_code == 201
        
    #make a good transaction, see what happens is not called
    transactionOne = {
            "product_id": 1,
            "supplier_id": 1,
            "type": "OUT",
            "quantity": 1,
        }

    transaction_response = client.post("/transactions", json=transactionOne)
    
        #does the transaction complete? Yes
    assert transaction_response.status_code == 201


    #testing the list with one transaction
    response = client.get("/transactions")

    assert response.status_code == 200
    #assert response.get_json()["supplier_id"] == 1
    #assert data["product_id"] == 1
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["product_id"] == 1
    assert data[0]["type"] == "OUT"
    assert data[0]["quantity"] == 1
    assert data[0]["supplier_id"] == 1

#testing two transactions

def test_get_supplier(client):

    #Find a supplier that doesn't exist
    response = client.get("/suppliers/1")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Supplier not found"

    #Make a supplier
    response = client.post(
            "/suppliers",
            json={
                "name": "Dell",
                "contact_email": "sales@dell.com"
            }
    
    
        )

    assert response.status_code == 201
    
    #find a supplier that exists
    response = client.get("/suppliers/1")
    assert response.status_code == 200
    data = response.get_json()
    #assert len(data) == 1
    assert data["name"] == "Dell"



#lets test a supplier
def test_update_supplier(client):
    #lets update a suppler that doesn't exist
    supplier_id = None
   
   
    response = client.put(
        f"/suppliers/{supplier_id}",
        json={
            "name": "Updated Name"
        }
    )
    #did it fail?
    assert response.status_code == 404


def test_supplier_products(client):
#make some test data
    product = {
            "name": "test",
            "sku": "test1",
            "unit_price": 1.00,
            "quantity_on_hand": 1,
        }
    #check it was created
    product_response = client.post("/products", json=product)
    assert product_response.status_code == 201
    
    # Create a test supplier
    supplier = {
            "name": "fakeSupplier",
            "contact_email": "test@test.com",
        }
    #check it was created 
    supplier_response = client.post("/suppliers", json=supplier)
    assert supplier_response.status_code == 201
        
    #In transaction
    transactionOne = {
            "product_id": 1,
            "supplier_id": 1,
            "type": "IN",
            "quantity": 1,
        }

    transaction_response = client.post("/transactions", json=transactionOne)
        #Test the notification
        #does the transaction complete? Yes
    assert transaction_response.status_code == 201

    #bad supplier
    response = client.get("/suppliers/999/products")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Supplier not found"

    #good supplier, good products
    response = client.get("/suppliers/1/products")
    #assert response.status.code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_purchase_order_defaults():
   #Make the purchase order
    po = PurchaseOrder(
        id=1,
        supplier_id=10,
        product_id=20,
        quantity_ordered=100
    )

    #Test the purchase order
    assert po.id == 1
    assert po.supplier_id == 10
    assert po.product_id == 20
    assert po.quantity_ordered == 100
    assert po.status == "pending"
    assert po.created_date == date.today()
    assert po.received_date is None





#suppliers_page_testing
#lets get to that 90
def test_suppliers_page_post(client):
    response = client.post(
        "/ui/suppliers",
        data={
            "name": "Dell",
            "contact_email": "dell@dell.com"
        }
    )

    assert response.status_code == 302
    assert len(store.suppliers) == 1

    supplier = next(iter(store.suppliers.values()))

    assert supplier.name == "Dell"
#delete_supplier_page

    response = client.post("/ui/suppliers/1/delete")

    #Is the supplier deleted
    assert response.status_code == 302

    assert 1 not in store.suppliers

#transactions_page
def test_transaction_increases_stock(client):
    #make some test data
    
    product = {
            "name": "test",
            "sku": "test1",
            "unit_price": 1.00,
            "quantity_on_hand": 10,
        }
    #check it was created
    product_response = client.post("/products", json=product)
    assert product_response.status_code == 201
    
    # Create a test supplier
    supplier = {
            "name": "fakeSupplier",
            "contact_email": "test@test.com",
        }
    #check it was created 
    supplier_response = client.post("/suppliers", json=supplier)
    assert supplier_response.status_code == 201

    #make an out transaction
    client.post(
        "/ui/transactions",
        data={
            "product_id": "1",
            "type": "OUT",
            "quantity": "5"
        }
    )

    #Make sure the Data is still good
    assert store.products[1].quantity_on_hand == 5
    assert len(store.transactions) == 1


