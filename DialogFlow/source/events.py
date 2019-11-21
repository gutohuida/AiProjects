from DbConector import DbConector
from config import MONGO_CONFIG as CONFIG
from datetime import date, datetime


def EventDate(EventName):
    db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")
    documment = db.findOne({"Name":unidecode(EventName)})
    if documment["Date"]:
        date = datetime.strptime(documment["Date"],'%Y-%m-%d')
        return date.strftime('%d de %B'), documment["Time"]
    return None, None   

def EventLocation(EventName):
    db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")
    documment = db.findOne({"Name":unidecode(EventName)})
    if documment["Location"]:
        return  documment["Location"]    
    return None

def Events():
    db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")
    documments = db.findAll({})
    events = []
    for documment in documments:
        events.append(documment["Name"])
    return events

def EventDescription(EventName):
    db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")    
    documment = db.findOne({"Name":unidecode(EventName)})
    return documment["Description"]