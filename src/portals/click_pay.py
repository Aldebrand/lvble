from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, TimeoutException
import re

from config import CLICK_PAY_URL, PAGE_LOAD_TIMEOUT
from utilities.logging_util import get_logger

logger = get_logger(__name__)

class ClickPayPortal:
    def __init__(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            logger.error(f"An error occurred while initializing the Click Pay portal scraper: {e}")
            raise e
        
    
    def _login(self, username, password):
        """
        Logs into the Click Pay portal using the provided username and password.

        Args:
            username (str): The username to use for logging in.
            password (str): The password to use for logging in.

        Raises:
            NoSuchElementException: If an element cannot be found.
            ElementNotInteractableException: If an element cannot be interacted with.
            ElementClickInterceptedException: If an element cannot be clicked.
            TimeoutException: If an element cannot be found within the timeout period.
            Exception: If an unexpected error occurs.
        """
        
        elements_indicators = {
            'login_link': '.login',
            'username_input': 'h_txt_Username',
            'password_input': 'h_txt_Password',
            'login_button': 'h_btn_Submit'
        }
        
        try:
            self.driver.get(CLICK_PAY_URL)
            #find the <a> tag with the class "login" and click it
            login_link = self.driver.find_element(By.CSS_SELECTOR, elements_indicators['login_link'])
            login_link.click()

            #find the <input> tag with the id "h_txt_Username" and enter the username
            username_input = self.driver.find_element(By.ID, elements_indicators['username_input'])
            username_input.send_keys(username)

            #find the <input> tag with the id "h_txt_Password" and enter the password
            password_input = self.driver.find_element(By.ID, elements_indicators['password_input'])
            password_input.send_keys(password)

            # find the <button> tag with the id "h_btn_Login" and click it
            login_button = self.driver.find_element(By.ID, elements_indicators['login_button'])
            login_button.click()
        except NoSuchElementException as e:
            logger.error(f"Failed to find element: {e}")
            raise e
        except ElementNotInteractableException as e:
            logger.error(f"Failed to interact with element: {e}")
            raise e
        except ElementClickInterceptedException as e:
            logger.error(f"Failed to click element: {e}")
            raise e
        except TimeoutException as e:
            logger.error(f"Timed out waiting for element: {e}")
            raise e
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e

    def _get_address(self):
            """
            Returns the address text from the page after waiting for it to load.

            Returns:
                str: The address text.

            Raises:
                TimeoutException: If the address element cannot be found within the timeout period.
            """
            def clean_up_address(address_text):
                """
                Cleans up the address text by removing leading/trailing whitespaces and empty lines.
                
                Args:
                    address_text (str): The address text to clean up.
                
                Returns:
                    str: The cleaned up address text.
                """
                # Split the text by lines, strip leading/trailing whitespaces, and filter out empty lines
                cleaned_lines = [line.strip() for line in address_text.split('\n') if line.strip()]
                # Join the cleaned lines back together with a space in between
                cleaned_address = ' '.join(cleaned_lines)
                # Replace multiple whitespace characters with a single space
                cleaned_address = re.sub(r'\s+', ' ', cleaned_address)

                return cleaned_address

            # wait until the page loads and the address is visible on the page
            try:
                address_span = WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "address"))
                )
            except TimeoutException as e:
                logger.error(f"Timed out waiting for address element: {e}")
                raise e
            
            address_text = clean_up_address(address_span.text)

            return address_text
    
    def _navigate_to_my_profile(self):
        """
        Navigates to the "My Profile" page.
        """
        element_indicators = {
            'dropdown': '//div[@class="rj-navigation-menu-navbar__dropdown" and @role="button"]',
            'my_profile_option': '//div[contains(@class, "rj-navigation-menu-navbar__dropdown-item") and text()="My Profile"]',
            'user_profile_page': '.card.col-12.rj-userProfile-content'
        }
        wait = WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT)

        try:
            # find the dropdown <div> tag with the class "rj-navigation-menu-navbar__dropdown-content"
            # and click it
            dropdown_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, element_indicators['dropdown']))
            )
            dropdown_button.click()

            # Wait until the dropdown menu is visible and then click the "My Profile" <div> tag
            my_profile_div = wait.until(
                EC.element_to_be_clickable((By.XPATH, element_indicators['my_profile_option']))
            )
            my_profile_div.click()

            # Wait until the "User Profile" page is loaded.
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_indicators['user_profile_page']))
            )
        except NoSuchElementException as e:
            logger.error(f"Failed to find element: {e}")
            raise e
        except ElementNotInteractableException as e:
            logger.error(f"Failed to interact with element: {e}")
            raise e
        except ElementClickInterceptedException as e:
            logger.error(f"Failed to click element: {e}")
            raise e
        except TimeoutException as e:
            logger.error(f"Timed out waiting for element: {e}")
            raise e
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e

    def _extract_contact_details(self):
        """
        Extracts the contact details from the "My Profile" page.
        
        Returns:
            dict: A dictionary containing the contact details:
                - email - The email address of the tenant.
                - phone - The phone number of the tenant.
        """
        # A dictionary to store the contact details
        contact_details = {}

        # A dictionary that maps the input field type to tuple of the input type and the aria-label
        info_labels = {
            'email': ('text', 'Email'),
            'phone': ('tel', 'Phone'),
        }

        def get_input_field_value(info_key, input_type, aria_label):
            """
            Gets the value of the input field with the given input type and aria-label.

            Args:
                info_key (str): The key to use for storing the value in the contact_details dictionary.
                input_type (str): The input type of the input field.
                aria_label (str): The aria-label of the input field.

            Returns:
                str: The value of the input field.
            """
            xpath_expression = f'//input[@type="{input_type}" and @aria-label="{aria_label}"]'
            try:
                input_field = self.driver.find_element(By.XPATH, xpath_expression)
                contact_details[info_key] = input_field.get_attribute('value')
            except NoSuchElementException:
                logger.warning(f"Failed to find input field with type '{input_type}' and aria-label '{aria_label}'")
                contact_details[info_key] = "Unknown"

        # Loop through the info_labels dictionary and extract the values of the input fields
        for info_key, (input_type, aria_label) in info_labels.items():
            get_input_field_value(info_key, input_type, aria_label)

        return contact_details
    
    def run(self, username, password):
        """
        Runs the Click Pay portal scraper.
        
        Args:
            username (str): The username to use for logging in.
            password (str): The password to use for logging in.
            
        Returns:
            dict: A dictionary containing the contact details:
                - address - The address of the tenant.
                - property_managment_company - The name of the property management company.
                - email - The email address of the tenant.
                - phone - The phone number of the tenant.
                or None if an error occurred.
        """
        try:
            self._login(username, password)
            address = self._get_address()
            self._navigate_to_my_profile()
            contact_details = self._extract_contact_details()
            contact_details['address'] = address

            return contact_details
        except Exception as e:
            logger.error(f"An error occurred while running the Click Pay portal scraper: {e}")
            
            return None
    
    def stop(self):
        """
        Stops the Click Pay portal scraper.
        """
        self.driver.quit()
    