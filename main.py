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
        # Initialize ChromeDriver using WebDriver Manager
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

        # Step 1: Dismiss popup
        time.sleep(3)
        try:
            cancel_button_xpath = '//*[@id="confirm"]/div/div[3]/a[2]'
            cancel_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, cancel_button_xpath))
            )
            cancel_button.click()
            logging.info("Popup dismissed.")
        except TimeoutException:
            logging.info("Popup did not appear.")

        # Step 2: Perform login
        try:
            username_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(os.getenv("USERNAME"))
            logging.info("Entered username.")

            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(os.getenv("PASSWORD"))
            logging.info("Entered password.")

            login_button_xpath = '//*[@class="pbutton blue registerSubmit"]'
            login_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, login_button_xpath))
            )
            login_button.click()
            logging.info("Clicked login button.")
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
            logging.error(f"Login failed: {e}")

        # Step 3: Post-login verification
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='some_element_after_login']"))
            )
            logging.info("Login successful.")
        except TimeoutException:
            logging.error("Login may have failed.")

        # Step 4: Set Availability
        try:
            # Example code for clicking availability options
            availability_button_xpath = '//*[@id="dashboardList"]/li[9]'
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, availability_button_xpath))
            ).click()
            logging.info("Clicked Availability button.")

            availability_option_xpath = '//*[@id="availabilityOption_chosen"]/a'
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, availability_option_xpath))
            ).click()
            logging.info("Opened availability dropdown.")

            available_option_xpath = '//*[@id="availabilityOption_chosen"]/div/ul/li[2]'
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, available_option_xpath))
            ).click()
            logging.info("Selected 'Available' option.")

            # Repeat similar steps for other dropdowns
        except Exception as e:
            logging.error(f"Setting availability failed: {e}")
    finally:
        driver.quit()
        logging.info("Browser closed.")

if __name__ == "__main__":
    main()
