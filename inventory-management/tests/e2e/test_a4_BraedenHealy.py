import uuid
from playwright.sync_api import expect

#Success Test (Workflow 1)
def test_adding_products(page):
    #Make product with a unique sku
    product = "Dummy"
    sku = "MakeProduct" + uuid.uuid4().hex[:8].upper()

    #Go to products
    page.goto("http://127.0.0.1:5000/ui/products")

    #Fill in product
    page.locator('input[name="name"]').fill(product)
    page.locator('input[name="sku"]').fill(sku)
    page.locator('input[name="unit_price"]').fill("10")
    page.locator('input[name="quantity_on_hand"]').fill("10")

    #Add product
    page.get_by_role("button", name="Add Product").click()

    #Ensure product exists in list
    check_product = page.locator("table tr").filter(has_text=sku)
    expect(check_product).to_be_visible()
    expect(check_product).to_contain_text(product)
    expect(check_product).to_contain_text("10")
    expect(check_product).to_contain_text("10")

#Error/Boundary Test (Workflow 2)
def test_transaction_quantity_too_large(page):
    #Make product with a unique sku
    product = "Dummy"
    sku = "BadTransaction" + uuid.uuid4().hex[:8].upper()

    #Go to products
    page.goto("http://127.0.0.1:5000/ui/products")

    #Fill products
    page.locator('input[name="name"]').fill(product)
    page.locator('input[name="sku"]').fill(sku)
    page.locator('input[name="unit_price"]').fill("10")
    page.locator('input[name="quantity_on_hand"]').fill("10")

    #Add product
    page.get_by_role("button", name="Add Product").click()

    #Ensure product exists in list
    check_product = page.locator("table tr").filter(has_text=sku)
    expect(check_product).to_be_visible()
    expect(check_product).to_contain_text(product)
    expect(check_product).to_contain_text("10")
    expect(check_product).to_contain_text("10")

    #Get product id for transaction
    product_id = check_product.locator("td").nth(0).inner_text()

    #Go to transactions
    page.goto("http://127.0.0.1:5000/ui/transactions")

    #Fill transactions
    page.locator('input[name="product_id"]').fill(product_id)
    page.locator('select[name="type"]').select_option("OUT")
    page.locator('input[name="quantity"]').fill("20")

    # Capture JavaScript alert
    with page.expect_event("dialog") as dialog_info:
        page.get_by_role("button", name="Record").click()

    dialog = dialog_info.value

    #Ensure error message is correct for invald out transaction
    assert dialog.message == "Not enough stock available!"
    dialog.accept()


    #Ensure stock unchanged after transaction
    page.goto("http://127.0.0.1:5000/ui/products")
    check_product = page.locator("table tr").filter(has_text=sku)
    expect(check_product.locator("td").nth(4)).to_have_text("10")