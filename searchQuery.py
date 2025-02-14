import requests

def main ():
    if not check_search_query():
        print("Search query is not injectable")
    
    # search query is injectable
    
def check_search_query():
    url = "http://localhost:3000/rest/products/search?q="

    # confirm we can reach the website
    try: 
        response = requests.get(url)

    except requests.exceptions.RequestException:
        print("Error occured while requesting " + url)
        return
    
    # test to see if it is injectable 
    url = "http://localhost:3000/rest/products/search?q=a\'"

    try:
        response = requests.get(url, headers={'Accept':'application/json'}) #as json
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # print raw error
        print("Error",e.response.json())

    json = response.json()
    code = json['error']['code']
    print(code)
    if code == "SQLITE_ERROR":
        return True
    return False


if __name__ == "__main__":
    main()

