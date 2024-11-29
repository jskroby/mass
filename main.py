import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  # Ensures Chrome runs in headless mode

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver
    except Exception as e:
        logging.error(f"Driver initialization failed: {e}")
        return None

def main():
    driver = initialize_driver()
    if not driver:
        return

    try:
        driver.get("https://v1.rentmasseur.com/login")
        logging.info("Website loaded successfully.")

        # Step 1: Login using environment variables
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        
        if not username or not password:
            logging.error("Environment variables for username or password are not set.")
            return

        try:
            username_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(username)
            logging.info("Entered username.")

            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            logging.info("Entered password.")

            login_button_xpath = '//*[@class="pbutton blue registerSubmit"]'
            login_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, login_button_xpath))
            )
            login_button.click()
            logging.info("Clicked login button.")
        except NoSuchElementException as e:
            logging.error("Login elements not found: " + str(e))
        except ElementClickInterceptedException as e:
            logging.error("Login button click was intercepted: " + str(e))
        except TimeoutException as e:
            logging.error("Timed out while trying to locate login elements: " + str(e))

        # Step 2: Post-login actions
        # Add further actions here...

    finally:
        driver.quit()
        logging.info("Bot execution completed. Browser closed.")

if __name__ == "__main__":
    main()
