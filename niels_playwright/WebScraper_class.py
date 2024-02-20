from playwright.sync_api import sync_playwright
import time


class WebScraper:
    def __init__(self, urls):
        # Initialize the url that is passed in
        self.urls = urls
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
        self.info = []
        self.hrefs = []
        self.results = []

    def get_results(self):
        # Initialize an empty list to store the results
        results = []

        # Iterate over the scraped data
        for i in range(len(self.overview)):
            # Create a dictionary for the current result
            result = {
                "address": {
                    "street_name": (
                        self.street_name[i] if i < len(self.street_name) else None
                    ),
                    "postal_code": (
                        self.postal_code[i] if i < len(self.postal_code) else None
                    ),
                    "town_name": self.town_name[i] if i < len(self.town_name) else None,
                },
                "description": (
                    self.description[i] if i < len(self.description) else None
                ),
                "info": self.info[i] if i < len(self.info) else None,
                "overview": self.overview[i] if i < len(self.overview) else None,
            }

            # Add the result to the list of results
            results.append(result)

        # Update the results attribute
        self.results = results

        # Return the results
        return self.results

    def click_button(self, page):
        try:
            # Check if the selector is found on the page
            if page.query_selector(self.button_selector):
                # If the selector is found, click it
                page.click(self.button_selector)
        except Exception as e:
            print(f"An error occurred while clicking the button: {e}")

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

        # Check if the address elements is None or empty
        if not address_elements:
            # If it's None or empty, skip this iteration
            return None

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

        # Return the address data
        return {
            "street_name": self.street_name,
            "postal_code": self.postal_code,
            "town_name": self.town_name,
        }

    def get_overview(self, page):
        # Get the overview element
        overview_element = page.query_selector(self.overview_selector)

        # Check if the overview element is None
        if not overview_element:
            # If it's None, skip this iteration
            return None

        # Get the text content of the overview element
        overview = overview_element.text_content().strip()

        # Add the overview to the list of overviews
        self.overview.append(overview)

        # Return the overview data
        return {"overview": self.overview}

    def get_description(self, page):
        # Get the description element
        description_element = page.query_selector(self.description_selector)

        # Check if the description element is None
        if description_element is None:
            # If it's None, skip this iteration
            return None

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

        # Return the description data
        return {"description": self.description}

    def get_info(self, page):
        # Get all elements with the class "classified-table__body"
        table_elements = page.query_selector_all(".classified-table__body")

        # Initialize an empty dictionary to store the info data
        info_data = {}

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
                    info_data[key] = value

        # Add the info data to the list of info
        self.info.append(info_data)

        # Return the info data
        return {"info": self.info}

    def scrape(self):
        with sync_playwright() as p:
            # Launch a new browser context
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            # Open a new page
            page = context.new_page()

            # Iterate over each url
            for url in self.urls:
                time.sleep(3)
                # Navigate to the page
                response = page.goto(url)

                # Check the status code of the response
                if response.status != 200:
                    print(f"Failed to load {url}, status code: {response.status}")
                    continue

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

                        # Get the results for this href
                        result = {
                            "address": self.get_address(page),
                            "overview": self.get_overview(page),
                            "description": self.get_description(page),
                            "info": self.get_info(page),
                        }

                        # Append the result to the results list
                        self.results.append(result)

                else:
                    print("No appartement available")

                    # Get the results for this url
                    result = {
                        "address": self.get_address(page),
                        "overview": self.get_overview(page),
                        "description": self.get_description(page),
                        "info": self.get_info(page),
                    }

                    # Append the result to the results list
                    self.results.append(result)

            # Close the page
            page.close()

            # Close the browser context
            context.close()

            # Close the browser
            browser.close()
