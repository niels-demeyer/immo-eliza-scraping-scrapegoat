from playwright.sync_api import sync_playwright


class WebScraper:
    def __init__(self, url):
        # Initialize the url that is passed in
        self.url = url
        # Initialize the selectors
        self.button_selector = 'button[data-testid="uc-accept-all-button"]'
        self.adress_selector = ".classified__information--address-row"
        self.overview_selector = ".overview__text"
        self.description_selector = ".classified__description"
        self.appartement_selector = (
            ".classified-with-plan__list-item.classified__list-item-link"
        )
        # Initialize the result variables
        self.street_name = []
        self.postal_code = []
        self.town_name = []
        self.overview = []
        self.description = []
        self.info = {}
        # Initialize the hrefs variable
        self.hrefs = []

    def click_button(self, page):
        page.wait_for_selector(self.button_selector)
        page.click(self.button_selector)

    def check_appartement(self, page):
        # Get all elements with the class "classified-with-plan__list-item classified__list-item-link"
        appartement_elements = page.query_selector_all(self.appartement_selector)

        # Clear the hrefs list
        self.hrefs.clear()

        # Iterate over each appartement element
        for appartement in appartement_elements:
            # Get the a tag in the appartement element
            a_tag = appartement.query_selector("a")

            # If the a tag exists
            if a_tag:
                # Get the href attribute of the a tag
                href = a_tag.get_attribute("href")

                # Add the href to the list
                self.hrefs.append(href)

        # Return the list of hrefs
        return self.hrefs

    def is_appartement_available(self, page):
        # Call the check_appartement method and store its output
        appartement_hrefs = self.check_appartement(page)

        # If the output is empty
        if not appartement_hrefs:
            # Return False
            return False

        # If the output is not empty
        # Return True
        return True

    def get_address(self, page):
        # Get all address elements
        address_elements = page.query_selector_all(self.adress_selector)

        # Iterate over each pair of address elements
        for i in range(0, len(address_elements), 2):
            # Get the text content of the first address element
            first_address = (
                address_elements[i]
                .text_content()
                .strip()
                .replace("\n", " ")
                .replace("—", "")
                .strip()
            )

            # Get the text content of the second address element
            second_address = (
                address_elements[i + 1]
                .text_content()
                .strip()
                .replace("\n", " ")
                .replace("—", "")
                .strip()
            )

            if second_address == "Ask for the exact address":
                # If the second address is "Ask for the exact address", set the street name to "Ask for the exact address"
                self.street_name.append(second_address)

                # The first address is the postal code and town name
                postal_code, town_name = first_address.split(maxsplit=1)
                self.postal_code.append(postal_code)
                self.town_name.append(town_name)
            else:
                # If the second address is not "Ask for the exact address", the first address is the street name
                self.street_name.append(first_address)

                # The second address is the postal code and town name
                postal_code, town_name = second_address.split(maxsplit=1)
                self.postal_code.append(postal_code)
                self.town_name.append(town_name)

    def get_overview(self, page):
        # Get all elements with the class "overview__text"
        overview_elements = page.query_selector_all(self.overview_selector)

        # Iterate over each overview element
        for element in overview_elements:
            # Get the text content of the overview element
            overview_text = (
                element.text_content()
                .strip()  # Remove leading/trailing whitespace
                .replace("\n", " ")  # Replace newlines with spaces
                .replace("—", "")  # Remove dashes
                .strip()  # Remove leading/trailing whitespace again
            )

            # Remove extra spaces
            overview_text = " ".join(overview_text.split())

            # Append the cleaned overview text to the overview list
            self.overview.append(overview_text)

    def get_description(self, page):
        # Get the description element
        description_element = page.query_selector(self.description_selector)

        # Get the text content of the description element
        description_text = (
            description_element.text_content()
            .strip()  # Remove leading/trailing whitespace
            .replace("\n", " ")  # Replace newlines with spaces
            .replace("—", "")  # Remove dashes
            .strip()  # Remove leading/trailing whitespace again
        )

        # Remove extra spaces
        description_text = " ".join(description_text.split())

        # Append the cleaned description text to the description list
        self.description.append(description_text)

    def get_info(self, page):
        # Get all elements with the class "classified-table__body"
        table_elements = page.query_selector_all(".classified-table__body")

        # Iterate over each table element
        for table in table_elements:
            # Get all rows in the table
            rows = table.query_selector_all(".classified-table__row")

            # Iterate over each row
            for row in rows:
                # Get the key cell in the row
                key_cell = row.query_selector("th.classified-table__header")
                # Get the value cell in the row
                value_cell = row.query_selector("td.classified-table__data")

                # If both cells exist
                if key_cell and value_cell:
                    # Get the text content of the key cell
                    key = key_cell.inner_text().strip()

                    # Get the text content of the value cell
                    value = value_cell.inner_text().strip()

                    # Store the key-value pair in the info dictionary
                    self.info[key] = value

    def scrape(self):
        with sync_playwright() as p:
            # Launch a new browser context
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # Open a new page
            page = context.new_page()

            # Navigate to the page
            page.goto(self.url)

            # Use the click_button method
            self.click_button(page)

            # Use the is_appartement_available method
            is_appartement = self.is_appartement_available(page)

            if is_appartement:
                print("Appartement is available")

                # Iterate over each href
                for href in self.hrefs:
                    # Navigate to the href
                    page.goto(href)

                    # Use the get_address method
                    self.get_address(page)

                    # Use the get_overview method
                    self.get_overview(page)

                    # Use the get_description method
                    self.get_description(page)

                    # Use the get_info method
                    self.get_info(page)

            else:
                print("No appartement available")

                # Use the get_address method
                self.get_address(page)

                # Use the get_overview method
                self.get_overview(page)

                # Use the get_description method
                self.get_description(page)

                # Use the get_info method
                self.get_info(page)

            # Close the browser context
            context.close()

            # Close the browser
            browser.close()


# Usage
scraper = WebScraper(
    # "https://www.immoweb.be/en/classified/villa/for-sale/brasschaat/2930/11095027"
    # "https://www.immoweb.be/en/classified/villa/for-sale/overijse/3090/11150716"
    "https://www.immoweb.be/en/classified/new-real-estate-project-apartments/for-sale/seraing/4100/11109402"
)
scraper.scrape()
print(scraper.street_name)
print(scraper.postal_code)
print(scraper.town_name)
print(scraper.overview)
print(scraper.description)
print(scraper.info)
