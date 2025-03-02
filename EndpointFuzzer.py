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

TEST_ENDPOINT1 = 'http://localhost:3000/'
TEST_ENDPOINT2 = 'http://localhost:3000/api/'
ENTRY_ENDPOINT = 'http://localhost:3000/#/'

exposed_endpoints_arr = []

driver = webdriver.Chrome()
# driver.install()
options = webdriver.ChromeOptions()

def simulate_user():

    driver.get(ENTRY_ENDPOINT)

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

def print_requests():
    print("\nGet requests found:\n")
    for request in driver.requests:
        if request.response:
            print(request.url)
    driver.quit()


async def run_fuzzer(url):

    with open("endpoints.txt", "r") as f:
        content = f.read()
        words = content.split()

    async with aiohttp.ClientSession() as session:
        tasks = []
        # loop through all words in file that we'll try and find endpoints with
        for word in words:
            task = request(word, session, url)
            tasks.append(task)    
        await asyncio.gather(*tasks)


async def request(word, session, url):
    # Send GET request to server 
    async with session.get(f'{url}{word}') as response:
        html = await response.text()   # request reponse

        if html and html[0] != '<':  # all front endpages begin with comment
            exposed_endpoints_arr.append(f'{url}{word}')  # add to array of found endpoints


def main():
    simulate_user()
    print_requests()
    print(f"\nChoosing these endpoints to fuzz test {TEST_ENDPOINT1} and {TEST_ENDPOINT2}")
    print("Running fuzz tester...\n")
    asyncio.run(run_fuzzer(TEST_ENDPOINT1))
    time.sleep(30)  # Give time for API endpoint to catch up
    asyncio.run(run_fuzzer(TEST_ENDPOINT2))
    print("Endpoints found:")
    print(exposed_endpoints_arr)

if __name__ == "__main__":
    main()