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
        # Initialize ChromeDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver
    except Exception as e:
        logging.error(f"Driver initialization failed: {e}")
        return None

def debug_save(driver, step_name):
    """Save a screenshot and page source for debugging."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = f"{step_name}_{timestamp}.png"
    page_source_path = f"{step_name}_{timestamp}.html"

    try:
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logging.error(f"Failed to save screenshot: {e}")

    try:
        with open(page_source_path, "w") as f:
            f.write(driver.page_source)
        logging.info(f"Page source saved: {page_source_path}")
    except Exception as e:
        logging.error(f"Failed to save page source: {e}")

def main():
    driver = initialize_driver()
    if not driver:
        return

    try:
        driver.get("https://v1.rentmasseur.com/login")
        logging.info("Website loaded successfully.")
        debug_save(driver, "login_page_loaded")

        # Step 1: Dismiss popup
        try:
            cancel_button_xpath = '//*[@id="confirm"]/div/div[3]/a[2]'
            cancel_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, cancel_button_xpath))
            )
            cancel_button.click()
            logging.info("Popup dismissed.")
        except TimeoutException:
            logging.info("Popup did not appear.")
        debug_save(driver, "post_popup_dismissal")

        # Step 2: Perform login
        try:
            username = os.getenv("USERNAME")
            password = os.getenv("PASSWORD")
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
        except Exception as e:
            logging.error(f"Login failed: {e}")
            debug_save(driver, "login_failed")

        # Step 3: Verify login
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='dashboardList']"))
            )
            logging.info("Login successful.")
        except TimeoutException:
            logging.error("Login may have failed. Verifying dashboard presence.")
            debug_save(driver, "login_verification_failed")

        # Additional steps can follow here...
    finally:
        debug_save(driver, "final_state")
        driver.quit()
        logging.info("Browser closed.")

if __name__ == "__main__":
    main()
