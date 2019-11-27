from core.DbConector import DbConector, Evento
from core.config import MONGO_CONFIG as CONFIG
from datetime import date, datetime
from unidecode import unidecode

import dateutil.parser

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