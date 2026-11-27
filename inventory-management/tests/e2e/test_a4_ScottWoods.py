from playwright.sync_api import Page, expect


class TestSupplierManagement:

    def test_add_supplier_with_valid_information(self, page: Page):
        # Navigate to supplier page
        page.goto("http://127.0.0.1:5000/ui/suppliers")

        
     #fill form with good data
  
        page.locator('input[name="name"]').fill('Acme Supplies')
        page.locator('input[name="contact_email"]').fill('contact@acme.com')


        # Save
        page.get_by_role("button", name="Add Supplier").click()

    
        # check it was saved
        expect(page.locator("table")).to_contain_text("Acme Supplies")
        expect(page.locator("table")).to_contain_text("contact@acme.com")
     

    def test_add_supplier_missing_required_information(self, page: Page):
        # Navigate to supplier page
        page.goto("http://127.0.0.1:5000/ui/suppliers")

    

        # Leave required fields blank

        nameField = page.locator('input[name="name"]')

        page.locator('input[name="name"]').fill('')
        

        #attempt to save
        page.get_by_role("button", name="Add Supplier").click()

     

        # Verify validation errors
        message = nameField.evaluate("el => el.validationMessage")
        assert "Please fill out this field." in message
 

        #fill one field to get to the other field. 
        page.locator('input[name="name"]').fill('Richard')

        #test the other field
        page.locator('input[name="contact_email"]').fill('bademail')

        page.get_by_role("button", name="Add Supplier").click()

        #verify the email
        emailField = page.locator('input[name="contact_email"]')
        message = emailField.evaluate("el => el.validationMessage")
        assert "Please include an '@' in the email address. 'bademail' is missing an '@'." in message

       #check to make sure the record wasn't added. 
        expect(page.locator("table")).not_to_contain_text("bademail")
        
    

    