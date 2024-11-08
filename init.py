import requests
import json
import os
from dotenv import load_dotenv
from dotenv import set_key
from datetime import datetime, timedelta
from event import Event

# TODO
# Obtain organization ID from search query
# Obtain primary contact for auth
# Obtain events from past three weeks 

load_dotenv()

NAME = "X-Engage-Api-Key"
KEY = os.getenv('API_KEY')
NUM_WEEKS = 3
headers = {
    NAME: KEY,
    'accept': 'application/json'
}

ROOT_URL = "https://engage-api.campuslabs.com/api/v3.0/"

org_name = input("Please provide your organization name: ")

# Only URLS for GET requests
REQUEST_URL = ROOT_URL + "/organizations/organization?isShownInPublicDirectory=true&name=" + org_name

response_org = requests.get(url=REQUEST_URL, headers=headers).json()

# Obtain the names of organizations from the search query
# DONE
print("Please choose from one of the organizations:")
i = 1
for item in response_org['items']:
    print(str(i) + ") " + item['name'])
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

three_weeks_ago = datetime.now() - timedelta(weeks=NUM_WEEKS)

response_events = requests.get(url=ROOT_URL + "/events/event?excludeCoHosts=true&includeSubmissionIds=false&organizationIds="+ org_id + "&IncludeRsvpCounts=false&startsAfter=" + three_weeks_ago.isoformat(), headers=headers).json()

events = []
for event in response_events['items']:
    events.append(Event(event['id'], event['name'], event['description'], event['imageUrl'], datetime.fromisoformat(event['startsOn']), datetime.fromisoformat(event['endsOn']), event['accessCode'], event['address']['name']))

i = 1
print("All Events from past " + str(NUM_WEEKS) + " weeks")
for event in events:
    print(str(i) + ") " + event.title + " held at " +  event.startsOn.strftime('%m/%d/%Y'))
    i += 1

