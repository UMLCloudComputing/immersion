# EDIT ME, file description
# Author: Gurpreet Singh
# © UML Cloud Computing Club 2024


import requests
import json
import os
from dotenv import load_dotenv
from dotenv import set_key
from datetime import datetime, timedelta
from data_objects.event import Event

# TODO
# Obtain organization ID from search query - DONE
# Obtain primary contact for auth - DONE
# Obtain events from past X weeks  - DONE
# Obtain organization finances
# Obtain 

load_dotenv()

NAME = "X-Engage-Api-Key"
KEY = os.getenv('API_KEY')
NUM_WEEKS = 3
headers = {
    NAME: KEY,
    'accept': 'application/json'
}

WRAPPER_KEY = '012345'

user_key = input("Please provide an Immersion API Key to authenticate your data transactions: ")
if not (user_key == WRAPPER_KEY):
    print("Bad access token, bearer did not authenticate correctly")
    exit(1)

ROOT_URL = os.getenv('ROOT_URL')
org_name = input("Please provide your organization name: ")

# Only URLS for GET requests
REQUEST_URL = ROOT_URL + "/organizations/organization?isShownInPublicDirectory=true&name=" + org_name

response_org = requests.get(url=REQUEST_URL, headers=headers).json()

# Obtain the names of organizations from the search query
# DONE
print("Please choose from one of the organizations:")
i = 1
for item in response_org['items']:
    print('   ' + str(i) + ") " + item['name'])
    i += 1

org_choice = int(input("Your Choice: ")) - 1

org_id = str(response_org['items'][org_choice]['id'])
print("Your organization ID: " + org_id)
set_key(".env", "ORG_ID", org_id)

# Obtain primary contact
contact_dump = response_org['items'][org_choice]['primaryContactId']
print("Primary contact raw dump:" + json.dumps(contact_dump, indent=4))
print("Primary contact email: " + contact_dump['campusEmail'])

# Obtain event data from past X weeks.

X_weeks_ago = datetime.now() - timedelta(weeks=NUM_WEEKS)

response_events = requests.get(url=ROOT_URL + "/events/event?excludeCoHosts=true&includeSubmissionIds=false&organizationIds="+ org_id + "&IncludeRsvpCounts=false&startsAfter=" + X_weeks_ago.isoformat(), headers=headers).json()

events = []
for event in response_events['items']:
    events.append(Event(event['id'], event['name'], event['description'], event['imageUrl'], datetime.fromisoformat(event['startsOn']), datetime.fromisoformat(event['endsOn']), event['accessCode'], event['address']['name']))

i = 1
print("All Events from past " + str(NUM_WEEKS) + " weeks")
for event in events:
    print('   ' + str(i) + ") " + event.title + " held at " +  event.startsOn.strftime('%m/%d/%Y'))
    i += 1

# Obtain current balance in club account
response_finance = requests.get(url=ROOT_URL + "/finance/account?organizationId=" + org_id, headers=headers).json()
balances = []
for item in response_finance['items']:
    balances.append((item['name'], item['availableFunds']))

print("Account '" + str(balances[0][0]) + "' has Balance $" + str(balances[0][1])) if len(balances) > 0 else print("There is no associated account from which to draw funds")
