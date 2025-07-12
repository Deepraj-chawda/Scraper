import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from urllib.robotparser import RobotFileParser


class BuildingConnectedScraper:
    def __init__(self, headless=True):
        self.base_url = "https://app.buildingconnected.com"
        self.login_url = f"{self.base_url}/login?retUrl=%2F"
        self.rate_limit = 3  # seconds between requests
        self.last_request_time = 0
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        # Configure browser options
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument(f'user-agent={self.user_agent}')
        options.add_argument('--disable-blink-features=AutomationControlled')

        self.driver = webdriver.Chrome(options=options)

    def enforce_rate_limit(self):
        """Ensure we respect rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def login(self, email, password):
        """Login to BuildingConnected account"""

        try:
            self.enforce_rate_limit()
            self.driver.get(self.login_url)
            time.sleep(4)

            # Wait for login form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "emailField"))
            )

            email_field = self.driver.find_element(By.ID, "emailField")
            email_field.send_keys(email)

            next_button = self.driver.find_element(By.XPATH, "//button[@aria-label='NEXT']")
            next_button.click()

            # wait for  verify form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "verify_user_btn"))
            )

            nextverify_button = self.driver.find_element(By.ID, "verify_user_btn")
            nextverify_button.click()
            time.sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            submit_button = self.driver.find_element(By.ID, "btnSubmit")
            submit_button.click()
            time.sleep(3)
            code = input("Enter your Verification Code sent to your mail: ")
            code_field = self.driver.find_element(By.ID, "VerificationCode")
            code_field.send_keys(code)

            submit_button = self.driver.find_element(By.ID, "btnSubmit")
            submit_button.click()

            print("Login successful")
            return True

        except TimeoutException:
            print("Timeout during login - check credentials or page structure")
            return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def extract_employee_data(self):
        try:
            self.enforce_rate_limit()
            self.driver.get('https://app.buildingconnected.com/companies/68525131d62066154bfd00ed/employees')
            container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ReactVirtualized__Grid__innerScrollContainer"))
            )

            # Find all employee rows
            rows = container.find_elements(By.CSS_SELECTOR, ".ReactVirtualized__Table__row")
            employees = []

            for row in rows:

                try:
                    # Extract name
                    name_element = row.find_element(By.CSS_SELECTOR, "[data-id='user-name']")
                    name = name_element.text

                    # Extract email
                    email_element = row.find_element(By.CSS_SELECTOR, "[data-id='employee-email']")
                    email = email_element.text

                    # Extract phone (if available)
                    try:
                        phone_element = row.find_element(By.CSS_SELECTOR, "[data-id='employee-phone']")
                        phone = phone_element.text
                    except:
                        phone = ""

                    # Extract title (if available)
                    try:
                        title_element = row.find_element(By.CSS_SELECTOR, "div[class*='title-'][title]")
                        title = title_element.text
                    except:
                        title = ""

                    # Extract initials and color
                    try:
                        avatar = row.find_element(By.CSS_SELECTOR, "[data-id='user-avatar']")
                        initials = avatar.text

                    except:
                        initials = ""

                    employees.append({
                        "initials": initials,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "title": title,
                        "is_lead": "Yes" if row.find_elements(By.CSS_SELECTOR,
                                                              "[data-id='toggle-lead-checkbox'][checked]") else "No"
                    })

                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue

            return employees

        except TimeoutException:
            print("Timed out waiting for employee data to load")
            return None
        except Exception as e:
            print(f"Error extracting employee data: {e}")
            return None

    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")

    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        if not data:
            return

        keys = data[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")

    def close(self):
        """Clean up resources"""
        self.driver.quit()


def main():
    # Get credentials
    email = input("Enter your BuildingConnected email: ")
    password = input("Enter your BuildingConnected password: ")

    scraper = BuildingConnectedScraper(headless=False)  # Set headless=True for production

    if scraper.login(email, password):
        data = scraper.extract_employee_data()

        if data:
            scraper.save_to_json(data, "buildingconnected_data.json")
            scraper.save_to_csv(data, "buildingconnected_data.csv")
        else:
            print("NO data extracted")

    scraper.close()


if __name__ == "__main__":
    main()