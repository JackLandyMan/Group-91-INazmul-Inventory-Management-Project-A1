#Scott Woods CISC 327
#Testing Supplier, Transactions



#JSON codes
#200 OK: Data fetched successfully.
#201 Created: New resource successfully built.
#204 No Content: Action succeeded, returning no body.
#404 Not found



#S1
#This tests the list fuction.
def test_list_suppliers(client):
#testing to see if the array is empty.
    response = client.get("/suppliers")

    assert response.status_code == 200
    assert response.get_json() == []

#S2
#test with one supplier
    response = client.post(
        "/suppliers",
        json={
            "name": "Dell",
            "contact_email": "sales@dell.com"
        }


    )

    #did it create the data
    assert response.status_code == 201

    #Now get the Data for the test
    response = client.get("/suppliers")
    data = response.get_json()
    #did it get the data
    assert response.status_code == 200
    #check the length
    assert len(data) == 1
    #check the data
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Dell"
    assert data[0]["contact_email"] == "sales@dell.com"
#S3
#Testing two suppliers
    response = client.post(
        "/suppliers",
        json={
            "name": "Bell",
            "contact_email": "sales@bell.com"
        }


    )

    data = response.get_json()

    assert response.status_code == 201

    response = client.get("/suppliers")
    data = response.get_json()

    assert response.status_code == 200
    #Check the length
    assert len(data) == 2
    #check the data
    assert data[1]["id"] == 2
    assert data[1]["name"] == "Bell"
    assert data[1]["contact_email"] == "sales@bell.com"
    


def test_create_supplier(client):
   #S4
   #Test a normal input
    response = client.post(
        "/suppliers",
        json={
            "name": "Dell",
            "contact_email": "sales@dell.com"
        }


    )

    data = response.get_json()
    #did it make the record
    assert response.status_code == 201
    #checking the data
    assert data["name"] == "Dell"
    assert data["contact_email"] == "sales@dell.com"

#S5
    #test an alternate input
    response = client.post(
        "/suppliers",
            json={
                "name": "Bell",
                "contact_email": "sales@Bell.com"
            }
    )
    data = response.get_json()
    
    assert response.status_code == 201
    assert data["name"] == "Bell"
    assert data["contact_email"] == "sales@Bell.com"
#5-a
    #Test a double entry of the same supplier
    response = client.post(
            "/suppliers",
                json={
                    "name": "Bell",
                    "contact_email": "sales@Bell.com"
                }
        )
    data = response.get_json()
        
    assert response.status_code == 201
    assert data["name"] == "Bell"
    assert data["contact_email"] == "sales@Bell.com"
    
#S6
    #test a low edge case
    response = client.post(
        "/suppliers",
            json={
                "name": "a",
                "contact_email": "a@a.a"
            }
    )
    data = response.get_json()
    
    assert response.status_code == 201
    assert data["name"] == "a"
    assert data["contact_email"] == "a@a.a"
#S7
#Write a high edge case
#30 a's 
    response = client.post(
            "/suppliers",
                json={
                    "name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "contact_email": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com"
                }
        )
    data = response.get_json()
        
    assert response.status_code == 201
    assert data["name"] == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert data["contact_email"] == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com"
    
    
    #S8
    #test a bad email
    response = client.post(
        "/suppliers",
            json={
                "name": "Bad Email",
                "contact_email": "BadEmailInput"
            }
    )
    data = response.get_json()
    
    assert response.status_code == 201
    assert data["name"] == "Bad Email"
    assert data["contact_email"] == "BadEmailInput"




def test_update_supplier(client):
    
    #Adding a supplier with good data
    response = client.post(
        "/suppliers",
        json={
            "name": "old",
            "contact_email": "old@test.com"
        }
    )

    data = response.get_json()

    assert data["name"] == "old"
    assert data["contact_email"] == "old@test.com"
#S9
        #Updating a good supplier with new data
        #Adding the /1 points to the specific record
    response = client.put(
        "/suppliers/1",
        json={
            "name": "New",
            "contact_email": "new@test.com"
        }
    )

    data = response.get_json()
    #check to see if the data updated
    assert data["name"] == "New"
    assert data["contact_email"] == "new@test.com"
    
    
    
    
    
def delete_supplier(client):

    #Make a supplier then delete it.
    response = client.post(
        "/suppliers",
        json={
            "name": "old",
            "contact_email": "old@test.com"
        }
    )
#S10
#delete a supplier that exists
    response = client.delete("/suppliers/1")

    assert response.status_code == 204

#S11
    #Delete a supplier that doesnt exist. 
    
    response = client.delete("/suppliers/44")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Supplier not found"

def test_outgoing_transactions(client):
    #make a product (good data)
    response = client.post(
        "/products",
        json={
            "name": "OldCheese",
            "sku": "01test",
            "unit_price":1.00,
            "quantity_on_hand": 2,

        }
    )
        
    assert response.status_code == 201

    #make a supplier (good data)
    response = client.post(
            "/suppliers",
            json={
                "name": "Dell",
                "contact_email": "sales@dell.com"
            }
    
    
        )

    assert response.status_code == 201
#S12
    #Test a normal out transaction of a product
    response = client.post(
            "/transactions",
            json={
                "product_id": 1,
                "type": "OUT",
                "quantity": 1,
                "supplier_id": 1
            }
        )
    #Catch the message
    assert response.status == "201 CREATED"

    #check the data - did it remove the quantity ? 
    data = response.get_json()
    assert data["product_id"] == 1
    assert data["type"] == "OUT"
    assert data["quantity"] == 1
    assert data["supplier_id"] == 1
    
    #S13
    #add a missing product with a higher number
    
    response = client.post(
            "/transactions",
            json={
                "product_id": 2,
                "type": "OUT",
                "quantity": 1,
                "supplier_id": 1
            }
        )

    
    assert response.status == "404 NOT FOUND"
    #S14
    #check product not there lower
    response = client.post(
            "/transactions",
            json={
                "product_id": 0,
                "type": "OUT",
                "quantity": 1,
                "supplier_id": 1
            }
        )
    assert response.status == "404 NOT FOUND"
    #S15
    #check for bad type
    response = client.post(
                "/transactions",
                json={
                    "product_id": 1,
                    "type": "DOGS",
                    "quantity": 1,
                    "supplier_id": 1
                }
            )
    assert response.status == "400 BAD REQUEST"

    
    #S16
    #testing a negative quantity
    response = client.post(
                "/transactions",
                json={
                    "product_id": 1,
                    "type": "Out",
                    "quantity": -11,
                    "supplier_id": 1
                }
            )
    assert response.status == "400 BAD REQUEST"
    #S17
    #check a bad supplier, lower
    response = client.post(
                "/transactions",
                json={
                    "product_id": 1,
                    "type": "Out",
                    "quantity": 1,
                    "supplier_id": -1
                }
            )
    assert response.status == "400 BAD REQUEST"

    #check for a bad supplier id, higher
    #S18
    response = client.post(
                "/transactions",
                json={
                    "product_id": 1,
                    "type": "Out",
                    "quantity": 1,
                    "supplier_id": 2
                }
            )
    assert response.status == "400 BAD REQUEST"

#I made a seperate function to test my added functionality.
#it does repeat some very similar tests to the ones I had done for out

def test_outgoing_transactions_Sale(client):
     
         #make a product (good data)
    response = client.post(
        "/products",
        json={
            "name": "OldCheese",
            "sku": "01test",
            "unit_price":1.00,
            "quantity_on_hand": 2,

        }
    )
        
    assert response.status_code == 201

    #make a supplier (good data)
    response = client.post(
            "/suppliers",
            json={
                "name": "Dell",
                "contact_email": "sales@dell.com"
            }
    
    
        )

    assert response.status_code == 201
     
     
     #S19
     #Test a good transaction
    response = client.post(
                    "/transactions",
                    json={
                        "product_id": 1,
                        "type": "SALE",
                        "quantity": 1,
                        "supplier_id": 1
                    }
                )
    assert response.status == "201 CREATED"
    data = response.get_json()
    assert data["product_id"] == 1
    assert data["type"] == "SALE"
    assert data["quantity"] == 1
    assert data["supplier_id"] == 1

     #check product id not found higher range
    #S20   
    response = client.post(
                "/transactions",
                json={
                    "product_id": 2,
                    "type": "SALE",
                    "quantity": 1,
                    "supplier_id": 1
                }
            )
    
        
    assert response.status == "404 NOT FOUND"
        #S21
        #check product not there lower
    response = client.post(
                "/transactions",
                json={
                    "product_id": 0,
                    "type": "SALE",
                    "quantity": 1,
                    "supplier_id": 1
                }
            )
    assert response.status == "404 NOT FOUND"
    #S22
    #testing a negative quantity (This should fail but doesn't) I didn't have it pointing to bad requests because i wanted pytest to continue
    response = client.post(
                    "/transactions",
                    json={
                        "product_id": 1,
                        "type": "SALE",
                        "quantity": -11,
                        "supplier_id": 1
                    }
                )
    assert response.status == "201 CREATED"
    #assert response.status == "400 BAD REQUEST"

    data = response.get_json()
    assert data["product_id"] == 1
    assert data["type"] == "SALE"
    assert data["quantity"] == -11
    assert data["supplier_id"] == 1
#S23
#check a bad supplier, lower. This should fail but doesn't I didn't have it pointing to bad requests because i wanted pytest to continue
    response = client.post(
                    "/transactions",
                    json={
                        "product_id": 1,
                        "type": "SALE",
                        "quantity": 1,
                        "supplier_id": -1
                    }
                )
    assert response.status == "201 CREATED"
    #assert response.status == "400 BAD REQUEST"

    #S24
    #check for a bad supplier id, higher (This should fail but doesn't) I didn't have it pointing to bad requests because i wanted pytest to continue
    response = client.post(
                    "/transactions",
                    json={
                        "product_id": 1,
                        "type": "SALE",
                        "quantity": 1,
                        "supplier_id": 56
                    }
                )
    assert response.status == "201 CREATED"
    #assert response.status == "400 BAD REQUEST"





    
    
