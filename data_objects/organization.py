# EDIT ME, file description
# Author: Gurpreet Singh
# © UML Cloud Computing Club 2024


import os
import requests
from dotenv import load_dotenv
from exceptions import KeyNotProvidedError
from primaryContact import PrimaryContact
from finance import FinanceAccount
ROOT_URL = os.getenv('ROOT_URL')

load_dotenv()

class Organization:
    """
    @params
    (int)   orgID: The Engage Organization ID

    @returns
    (Organization)  An organization object
    """
    def __init__(self, orgID:int) -> None:
        NAME = "X-Engage-Api-Key"
        KEY = os.getenv('API_KEY')
        self.headers = {
            NAME: KEY,
            'accept': 'application/json'
        }
        self.IMM_KEY = os.getenv('IMMERSION_KEY')
        if self.IMM_KEY == None:
            raise KeyNotProvidedError("Immersion API not provided")
        self.orgID = orgID
        self.orgData = requests.get(ROOT_URL + "/organizations/organization?isShownInPublicDirectory=true&ids=" + self.orgID).json()
        self.orgName = self.orgData['items'][0]['name']
        self.primaryContact = PrimaryContact(self.orgData['items'][0]['primaryContactId'])

    
    # TODO
    # Send authentication code to primary contact
    # def authenticate(self):
    
    """
    Obtain list of Finance Account objects for your club
    Uses HTTP requests to fetch live data
    @params
    None

    @returns
    (list[FinanceAccount])      A List of FinanceAccount objects for the organization 
    """
    def getFinanceAccounts(self):
        response_finance = requests.get(ROOT_URL + "/finance/account?organizationId=" + str(self.orgID))
        return [FinanceAccount(account) for account in response_finance['items']]

    
        
