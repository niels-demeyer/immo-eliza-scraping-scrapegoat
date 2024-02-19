from playwright.sync_api import sync_playwright

button_selector = 'button[data-testid="uc-accept-all-button"]'
adress_selector = '.classified__information--address-row'

with sync_playwright() as p:
    # Launch a new browser context
    browser = p.chromium.launch(headless=False)  
    context = browser.new_context()

    # Open a new page
    page = context.new_page()

    # Navigate to the page
    page.goto("https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/11095027")

    # Click the button
    page.wait_for_selector(button_selector)
    page.click(button_selector)

    # Wait for the address element to be present and get its text
    address_element = page.wait_for_selector(adress_selector)
    address = address_element.text_content().strip()  # Remove leading and trailing whitespaces
    address = address.replace("\n", " ").replace("—", "").strip()  # Remove newline characters and dashes, then strip again

    # Split the address into postal_code and town_name
    postal_code, town_name = address.split()

    # Print the postal_code and town_name
    print(postal_code)
    print(town_name)

    # Close the browser
    browser.close()