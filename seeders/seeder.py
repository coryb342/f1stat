import requests
import json
import time
from db import establish_connection

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def get_json_response(url, max_attempts = 5):
    for attempt in range(max_attempts):
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        
        if response.status_code == 429:
            wait = 2 ** attempt
            print(f"Gotta slow down. Wait {wait} seconds to retry {url}")
            time.sleep(wait)
            continue

        print(f"Something is wrong: {response.status_code}")
        return