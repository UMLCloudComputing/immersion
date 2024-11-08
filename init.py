import requests
import json
import os
from dotenv import load_dotenv
from dotenv import set_key

# TODO
# Obtain organization ID from search query
# Obtain primary contact for auth

load_dotenv()

NAME = "X-Engage-Api-Key"
KEY = os.getenv('API_KEY')

headers = {
    NAME: KEY,
    'accept': 'application/json'
}

ROOT_URL = "https://engage-api.campuslabs.com/api/v3.0/"

org_name = input("Please provide your organization name: ")

# Only URLS for GET requests
REQUEST_URL = ROOT_URL + "/organizations/organization?isShownInPublicDirectory=true&name=" + org_name

response_data = requests.get(url=REQUEST_URL, headers=headers).json()

# Obtain the names of organizations from the search query
# DONE
print("Please choose from one of the organizations:")
i = 1
for item in response_data['items']:
    print(str(i) + ") " + item['name'])
    i += 1

org_choice = int(input("Your Choice: ")) - 1

org_id = str(response_data['items'][org_choice]['id'])
print("Your organization ID: " + org_id)
set_key(".env", "ORG_ID", org_id)

# Obtain primary contact
contact_dump = response_data['items'][org_choice]['primaryContactId']
print("Primary contact raw dump:" + json.dumps(contact_dump, indent=4))
print("Primary contact email: " + contact_dump['campusEmail'])