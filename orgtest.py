import requests
import json
import os
from dotenv import load_dotenv


# TODO
# HTTP requests to obtain organization ID from search query
# Obtain primary contact information for verification

load_dotenv()

NAME = "X-Engage-Api-Key"
KEY = os.getenv('API_KEY')

headers = {
    NAME: KEY,
    'accept': 'application/json'
}

ROOT_URL = "https://engage-api.campuslabs.com/api/v3.0/"



response = requests.get('https://engage-api.campuslabs.com/api/v3.0/events/event?excludeCoHosts=true&includeSubmissionIds=true&IncludeRsvpCounts=true', headers=headers)


response_dict = response.json()
print(response_dict['items'][0]['description'])
test_file = open('test.txt', 'w')
test_file.write("Name: " + response_dict['items'][0]['name'] + '\n')
test_file.write("Description: " + response_dict['items'][0]['description']  + '\n')
test_file.close()