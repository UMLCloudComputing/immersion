import json

class FinanceAccount:
    """
    Constructor for Finance Account object
    
    @params
    (json)              jsonDump: Raw JSON dump of finance account info from Engage

    @returns
    (FinanceAccount)    A FinanceAccount object
    """
    def __init__(self, jsonDump:json) -> None:
        self.name = jsonDump['name']
        self.desc = jsonDump['description']
        self.balance = jsonDump['balance']
        self.availableFunds = jsonDump['availableFunds']
