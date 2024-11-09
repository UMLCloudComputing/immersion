import json

class PrimaryContact:
    """
    Contruct Primary contact data from raw JSON dump of Engage API
    Only content held is:
        - accountID
        - username
        - campusEmail
    @params
    (json)              jsonDump: Raw JSON dump of primary contact info from Engage

    @returns
    (PrimaryContact)    A Primary Contact object
    """
    def __init__(self, jsonDump:json) -> None:
        self.accountID = jsonDump['accountId']
        self.username = jsonDump['username']
        self.campusEmail = jsonDump['campusEmail']
    