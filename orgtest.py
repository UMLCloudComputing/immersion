# Reads the event json file and creates a condensed version of it

import requests
import json
import os
from dotenv import load_dotenv

class orgtest:
    """
    Intialization for creating an Event object
    @params:
    (str)       eventID: Engage Event ID
    (str)       title: event publication title
    (str)       description: event description
    (str)       imageUrl: Event icongraphy/image URL
    (datetime)  startsOn: datetime object of start time
    (datetime)  endsOn: datetime object of the end time
    (str)       accessCode: Event activation code for Campus Labs Check-in
    (str)       location: Event location

    @returns:
    (Event)     Event object
    """
    load_dotenv()

    def __init__(self, eventID:str, title:str,  desc:str, imageUrl:str, startsOn:datetime, endsOn:datetime, accessCode:str, location:str) -> None:
        NAME = 'X-Engage-Api-Key'
        KEY = os.getenv('API_KEY')
        headers = {
            NAME: KEY,
            'accept': 'application/json'
        }
        self.ROOT_URL = 'https://engage-api.campuslabs.com/api/v3.0/'
        response = requests.get('https://engage-api.campuslabs.com/api/v3.0/events/event?excludeCoHosts=true&includeSubmissionIds=true&IncludeRsvpCounts=true', headers=headers)
        eventData = response.json()
                
        self.eventID = eventData['items'][0]['id']
        self.title = eventData['items'][0]['name']
        self.desc = eventData['items'][0]['description']
        self.imageUrl = eventData['items'][0]['imageUrl']
        self.startsOn = eventData['items'][0]['startsOn']
        self.endsOn = eventData['items'][0]['endsOn']
        self.accessCode = eventData['items'][0]['accessCode']
        self.location = eventData['items'][0]['address']['address']