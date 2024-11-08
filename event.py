from datetime import datetime
class Event:
    """
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
    def __init__(self, eventID:str, title:str,  desc:str, imageUrl:str, startsOn:datetime, endsOn:datetime, accessCode:str, location:str) -> None:
        self.eventID = eventID
        self.title = title
        self.desc = desc
        self.imageUrl = imageUrl
        self.startsOn = startsOn
        self.endsOn = endsOn
        self.accessCode = accessCode
        self.location = location
    
