import requests
import json

NAME = "X-Engage-Api-Key"
KEY = "esk_test_7772a5488f56d5def2dc911f5e54e5b2"

headers = {
    "Name": NAME,
    "Value": KEY
}
ROOT_URL = "https://engage-api.campuslabs.com/api/v3.0/"

# Only URLS for GET requests
URLS = {
    "events/category": ROOT_URL + "events/category",
    "events/events/": ROOT_URL + ""
}

response = requests.get(URLS['events/'], headers=headers)

response_data = response.json()

print(response_data['items'][1]['userId']['username'])
print(response_data['items'][0]['userId']['swipeCardIdentifier'])

# org_name = input("Please provide your organization's name:")
