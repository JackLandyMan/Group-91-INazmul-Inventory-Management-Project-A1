#Scott Woods CISC 327
#Testing Supplier, Transactions



#JSON codes
#200 OK: Data fetched successfully.
#201 Created: New resource successfully built.
#204 No Content: Action succeeded, returning no body.



 
#This tests the list fuction.
def test_list_suppliers(client):
#testing to see if the array is empty.
    response = client.get("/suppliers")

    assert response.status_code == 200
    assert response.get_json() == []

    #test with one supplier
    response = client.post(
        "/suppliers",
        json={
            "name": "Dell",
            "contact_email": "sales@dell.com"
        }


    )

    data = response.get_json()
    #did it create the data
    assert response.status_code == 201

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

    response = client.delete("/suppliers/1")

    assert response.status_code == 204

    #Delete a supplier that doesnt exist. 
    
    response = client.delete("/suppliers/44")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Supplier not found"

def test_outgoing_transactions(client):
    #make a product
    response = client.post(
        "/products",
        json={
            "name": "OldCheese",
            "sku": "01test",
            "unit_price":0.00,
            "quantity_on_hand": 6,

        }
    )


    assert response.status_code == 201

    #Test a normal removal of a product

