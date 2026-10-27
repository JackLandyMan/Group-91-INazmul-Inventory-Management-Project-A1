#Scott Woods CISC 327
#Testing Supplier, Transactions



#JSON codes
#200 OK: Data fetched successfully.
#201 Created: New resource successfully built.
#204 No Content: Action succeeded, returning no body.



#testing to see if the array is empty. 

def test_list_suppliers(client):

    response = client.get("/suppliers")

    assert response.status_code == 200
    assert response.get_json() == []


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

    assert response.status_code == 201
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




#def test_update_supplier(client):

#def test_delete_supplier(client):

#def test_list_transactions(client):
