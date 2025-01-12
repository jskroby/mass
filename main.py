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
        # Initialize ChromeDriver without specifying a version
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        return driver
    except Exception as e:
        print(f"Driver initialization failed: {e}")
        return None

def main():
    driver = initialize_driver()
    if not driver:
        return

    try:
        driver.get("https://v1.rentmasseur.com/login")
        logging.info("Website loaded successfully.")

        # Step 1: Wait for Popup and Close it if Present
        time.sleep(3)
        try:
            cancel_button_xpath = '//*[@id="confirm"]/div/div[3]/a[2]'
            cancel_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, cancel_button_xpath))
            )
            cancel_button.click()
            logging.info("Popup dismissed by clicking 'Cancel'.")
        except TimeoutException:
            logging.warning("Popup did not appear, continuing to login.")

        # Step 2: Perform Login
        try:
            username_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys("karpathianwolf")
            logging.info("Entered username.")

            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys("Lola369!")
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

        # Step 3: Post-login verification
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='some_element_after_login']"))
            )
            logging.info("Login successful.")
        except TimeoutException:
            logging.error("Login may have failed. Expected element not found post-login.")

        # Step 4: Click the Availability button on the Dashboard
        try:
            availability_button_xpath = '//*[@id="dashboardList"]/li[9]'
            availability_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, availability_button_xpath))
            )
            availability_button.click()
            logging.info("Clicked Availability button on the dashboard.")
            time.sleep(3)
            # Step 5: Open availability dropdown and select "Available"
            availability_option_xpath = '//*[@id="availabilityOption_chosen"]/a'
            availability_option_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, availability_option_xpath))
            )
            availability_option_button.click()
            logging.info("Opened availability option dropdown.")

            available_option_xpath = '//*[@id="availabilityOption_chosen"]/div/ul/li[2]'  # Assuming 2nd item is 'Available'
            available_option = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, available_option_xpath))
            )
            available_option.click()
            logging.info("Selected 'Available' option.")
            time.sleep(3)
            # Step 6: Open time dropdown and select "6 Hours"
            availability_time_xpath = '//*[@id="availabilityTime_chosen"]'
            availability_time_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, availability_time_xpath))
            )
            availability_time_button.click()
            logging.info("Opened availability time dropdown.")

            six_hours_option_xpath = '//*[@id="availabilityTime_chosen"]/div/ul/li[6]'  # 6th item for "6 Hours"
            six_hours_option = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, six_hours_option_xpath))
            )
            six_hours_option.click()
            logging.info("Selected '6 Hours' option.")
            time.sleep(3)
            # Step 7: Click "Set Now"
            set_now_button_xpath = '//*[@id="confirm"]/div/div[3]/a[1]'
            set_now_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, set_now_button_xpath))
            )
            set_now_button.click()
            logging.info("Clicked 'Set Now' button on the availability popup.")

        except TimeoutException:
            logging.error("Failed to locate or click elements for Availability or Set Now.")
        except ElementClickInterceptedException as e:
            logging.error("Element click was intercepted: " + str(e))

    finally:
        logging.info("Bot execution completed. Browser remains open for inspection.")
        # Remove driver.quit() if you want to keep the browser open.
        # driver.quit()

if __name__ == "__main__":
    main()
