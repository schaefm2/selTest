from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import aiohttp
import asyncio
import aiohttp
import asyncio

def simulate_user(entry_endpoint, driver):

    try:
        driver.get(entry_endpoint)

        banner_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mat-dialog-0"]/app-welcome-banner/div/div[2]/button[2]'))
        )
        banner_button.click()

        search = driver.find_element(By.XPATH, '//*[@id="searchQuery"]')
        search.click()

        search_input = driver.find_element(By.XPATH, '//*[@id="mat-input-0"]')
        search_input.send_keys('asdfasd')
        search_input.send_keys('\ue007') # search

        home = driver.find_element(By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-navbar/mat-toolbar/mat-toolbar-row/button[2]')
        home.click()

        applejuice = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/app-search-result/div/div/div[2]/mat-grid-list/div/mat-grid-tile[1]/div/mat-card/div[1]'))
        )
        applejuice.click()
    except error:
        print("Error in script please rerun")
        return False



def print_requests(driver):
    print("\nGet requests found:\n")
    for request in driver.requests:
        if request.response:
            print(request.url)
    driver.quit()


async def run_fuzzer(url, exposed_endpoints_arr):
    
    with open("endpoints.txt", "r") as f:
        content = f.read()
        words = content.split()

    async with aiohttp.ClientSession() as session:
        tasks = []
        # loop through all words in file that we'll try and find endpoints with
        for word in words:
            print(f'{url}{word}')
            task = request(word, session, url, exposed_endpoints_arr)
            tasks.append(task)    
        await asyncio.gather(*tasks)


async def request(word, session, url, exposed_endpoints_arr):
    # Send GET request to server 
    async with session.get(f'{url}{word}') as response:
        html = await response.text()   # request reponse

        if html and html[0] != '<':  # all front endpages begin with comment
            exposed_endpoints_arr.append(f'{url}{word}')  # add to array of found endpoints


def main():
    TEST_ENDPOINT1 = 'http://localhost:3000/'
    TEST_ENDPOINT2 = 'http://localhost:3000/api/'
    ENTRY_ENDPOINT = 'http://localhost:3000/#/'

    exposed_endpoints_arr = []
    driver = webdriver.Chrome()

        # catch errors in script
    if (simulate_user(entry_endpoint=ENTRY_ENDPOINT, driver=driver) == False):
        return
        
    print_requests(driver=driver)
    print(f"\nChoosing these endpoints to fuzz test {TEST_ENDPOINT1} and {TEST_ENDPOINT2}")
    input("Click Enter to begin running fuzz tester")
    asyncio.run(run_fuzzer(TEST_ENDPOINT1, exposed_endpoints_arr))
    print("Letting API endpoint catch up on requests")
    exposed_endpoints_arr.clear()
    time.sleep(30)  # Give time for API endpoint to catch up
    asyncio.run(run_fuzzer(TEST_ENDPOINT2, exposed_endpoints_arr))
    print("\nWaiting for requests to return\n")
    print("Endpoints found:")
    print(exposed_endpoints_arr)

if __name__ == "__main__":
    main()