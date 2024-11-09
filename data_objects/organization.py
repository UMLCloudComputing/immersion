# EDIT ME, file description
# Author: Gurpreet Singh
# © UML Cloud Computing Club 2024


import os
from dotenv import load_dotenv
load_dotenv()
from exceptions import KeyValidationError
class Organization:
    """
    @params
    (int)   orgID: The Engage Organization ID
    """
    def __init__(self, orgID:int, primaryContact:str) -> None:
        
        NAME = "X-Engage-Api-Key"
        KEY = os.getenv('API_KEY')
        self.IMM_KEY = os.getenv('IMMERSION_KEY')
        self.orgID = orgID
        self.primaryContact = primaryContact
        self.headers = {
            NAME: KEY,
            'accept': 'application/json'
        }

    
    # TODO
    # Send authentication code to primary contact
    # def authenticate(self):
    
    
    """
    Procedure to validate Immersion API key and throw exceptions
    @params
    (int)                   ImmersionAPIKey: The Immersion API key provided by the requester
    
    @throws
    (KeyValidationError)    An custom 'KeyValdiationError' exception 

    @returns
    None
    """
    def validateKey(self, ImmersionAPIKey: int):
        if not (ImmersionAPIKey == self.IMM_KEY):
            raise KeyValidationError("Bad access token, bearer did not authenticate correctly", "Code 200")
    
    """
    Obtain list of Finance Account objects for your club

    @params
    (int)       ImmersionAPIKey: The Immersion API key provided by the requestor

    @returns
    (list[FinanceAccount])      A List of 
    """
    def getFinanceAccounts(self, ImmersionAPIKey: int):
        
        try:
            self.validateKey("ImmersionAPIKey")
        except KeyValidationError as e:
            print(e.message)
            return


        
