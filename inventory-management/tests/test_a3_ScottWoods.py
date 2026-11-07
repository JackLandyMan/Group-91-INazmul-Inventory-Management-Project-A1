from unittest.mock import patch
from app import store
#Assignment 3 tests Scott Woods

#testing the failures
def test_notification_failure(monkeypatch, client):
    with patch("app.routes.transactions.send_notification", return_value=False) as mock_send:
        
        #make test data
        product = {
            "name": "test",
            "sku": "test1",
            "unit_price": 1.00,
            "quantity_on_hand": 5,
        }
    
        product_response = client.post("/products", json=product)
        assert product_response.status_code == 201
    
        # Create the dummy product
        supplier = {
            "name": "fakeSupplier",
            "contact_email": "test@test.com",
        }
    
        supplier_response = client.post("/suppliers", json=supplier)
        assert supplier_response.status_code == 201
        

        #assert transaction_response.get_json()["notification_sent"] == True
       
        #make a good transaction, see what happens when the notification fails
        transactionOne = {
            "product_id": 1,
            "supplier_id": 1,
            "type": "SALE",
            "quantity": 3,
        }

        transaction_response = client.post("/transactions", json=transactionOne)
        #Test the notification
        #does the transaction complete? Yes
        assert transaction_response.status_code == 201
        #did notification fail? Yes
        assert transaction_response.get_json()["notification_sent"] == False
        mock_send.assert_called_once()


        
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

       

#def test_list_suppliers(client):
#testing to see if the array is empty.
#    response = client.get("/suppliers")

#    assert response.status_code == 200
#    assert response.get_json() == []
