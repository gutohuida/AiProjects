from core.DbConector import DbConector, Evento
from core.config import MONGO_CONFIG as CONFIG
from datetime import date, datetime
from unidecode import unidecode

import dateutil.parser

# def EventDate(EventName):
#     db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")
#     documment = db.findOne({"Name":unidecode(EventName)})
#     if documment["Date"]:
#         date = datetime.strptime(documment["Date"],'%Y-%m-%d')
#         return date.strftime('%d de %B'), documment["Time"]
#     return None, None   

# def EventLocation(EventName):
#     db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")
#     documment = db.findOne({"Name":unidecode(EventName)})
#     if documment["Location"]:
#         return  documment["Location"]    
#     return None

# def Events():
#     db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")
#     documments = db.findAll({})
#     events = []
#     for documment in documments:
#         events.append(documment["Name"])
#     return events

# def EventDescription(EventName):
#     db = DbConector(CONFIG["host"],CONFIG["port"],CONFIG["db_name"],"Events")    
#     documment = db.findOne({"Name":unidecode(EventName)})
#     return documment["Description"]

def EventDate(EventName):
    documment = Evento.query.filter_by(evento_nome=EventName).first()
    if documment.evento_data:
        date = dateutil.parser.parse(str(documment.evento_data)).date()
        time = dateutil.parser.parse(str(documment.evento_data)).time()
        return date.strftime('%d de %B'), time
    return None, None   

def EventLocation(EventName):
    documment = Evento.query.filter_by(evento_nome=EventName).first()
    if documment:
        return  documment.evento_local
    return None

def Events():
    documments = Evento.query.distinct(Evento.evento_nome)
    events = []
    for documment in documments:
        events.append(documment.evento_nome)
    return events

def EventDescription(EventName):
    documment = Evento.query.filter_by(evento_nome=EventName).first()
    return documment.evento_desc