import time
import aiohttp
import asyncio
import aiohttp
import asyncio

TEST_ENDPOINT1 = 'http://localhost:3000/'

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



def main():
    print("Sending API requests")
    print("Check how application is handling being flooded with requests")
    print("Close program when finished")
    while True:
        asyncio.run(run_fuzzer(TEST_ENDPOINT1))
        time.sleep(30)  # Give time for API endpoint to catch up
    
if __name__ == "__main__":
    main()