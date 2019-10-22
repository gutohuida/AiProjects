# -*- coding: utf-8 -*-

# import flask dependencies
from flask import Flask, request, make_response, jsonify
from DbConector import DbConector
from datetime import date, datetime
from unidecode import unidecode
import json
import locale
import logging

#Horario brasileiro
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

#Read config
with open('./config.json') as file:
    config = json.load(file)


# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'


def EventDate(EventName):
    db = DbConector(config["host"],config["port"],config["db_name"],"Events")
    documment = db.findOne({"Name":unidecode(EventName)})
    if documment["Date"]:
        date = datetime.strptime(documment["Date"],'%Y-%m-%d')
        return date.strftime('%d de %B'), documment["Time"]
    return None, None   

def EventLocation(EventName):
    db = DbConector(config["host"],config["port"],config["db_name"],"Events")
    documment = db.findOne({"Name":unidecode(EventName)})
    if documment["Location"]:
        return  documment["Location"]    
    return None

def Events():
    db = DbConector(config["host"],config["port"],config["db_name"],"Events")
    documments = db.findAll({})
    events = []
    for documment in documments:
        events.append(documment["Name"])
    return events

def EventDescription(EventName):
    db = DbConector(config["host"],config["port"],config["db_name"],"Events")    
    documment = db.findOne({"Name":unidecode(EventName)})
    return documment["Description"]

#main webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    
    ##Verifica a data de um evento especifico
    if intent == "EventDate":
        date, time = EventDate(req["queryResult"]["parameters"]["Events"])
        if date:
            return jsonify({"fulfillmentText":"O próximo {0} acontecerá dia {1} as {2}. O que mais eu posso fazer por você?".format(req["queryResult"]["parameters"]["Events"],date,time)})
        return jsonify({"fulfillmentText": "O próximo {0} ainda não tem data marcada. O que mais eu posso fazer por você?".format(req["queryResult"]["parameters"]["Events"])})

    ##Verifica a data de um evento caso ele esteja no branch local ou consulta de evento especifico
    if intent == "EventLocationDate" or intent == "EventConsultDate":
        for value in req["queryResult"]["outputContexts"]:
            if value["name"].endswith("eventlocation-followup") or value["name"].endswith("eventconsult-followup"):
                event = value["parameters"]["Events"]

        date, time = EventDate(event)
        if date:
            return jsonify({"fulfillmentText":"Será no dia {0} as {1}. O que mais você precisa?".format(date,time)})
        return jsonify({"fulfillmentText": "Ainda não possui data marcada. O que mais você precisa?"})

    ##Verifica o local de um evento especifico
    if intent == "EventLocation":
        location = EventLocation(req["queryResult"]["parameters"]["Events"])
        if location:
            return jsonify({"fulfillmentText": "O {0} acontecerá no {1}. No que mais eu posso ajudar?".format(req["queryResult"]["parameters"]["Events"],location)})
        return jsonify({"fulfillmentText": "O {0} ainda não tem local definido. No que mais eu posso ajudar?".format(req["queryResult"]["parameters"]["Events"])})

    ##Verifica o local de um evento caso ele esteja no branch de data 
    if intent == "EventDateLocal":
        for value in req["queryResult"]["outputContexts"]:
            if value["name"].endswith("eventdate-followup"):
                event = value["parameters"]["Events"]

        location = EventLocation(event)
        if location:
            return jsonify({"fulfillmentText": "Será no {0}. O que mais eu posso fazer por você?".format(location)})
        return jsonify({"fulfillmentText": "Ainda não tem local definido. O que mais eu posso fazer por você?"})

    ##Consulta quais iniciativas o GBG possui
    if intent == "Events":
        events = Events()
        return jsonify({"fulfillmentText": "O GBG Curitiba possui as seguintes iniciativas: {0}. Gostaria de saber mais sobre alguma delas?".format(', '.join(events))} )

    ##Retorna a descrição de um evento dentro dos brachs de consulta de evento geral ou especifico
    if intent == "EventsYes" or intent == "EventConsult":
        if "outputContexts" in req["queryResult"]:
            for value in req["queryResult"]["outputContexts"]:
                if value["name"].endswith("events-followup") or value["name"].endswith("eventconsult-followup"):
                    event = value["parameters"]["Events"]
        else:
            event = req["queryResult"]["parameters"]["Events"]

        eventDescription = EventDescription(event)
        return jsonify({"fulfillmentText":'{0} No que mais eu posso ajudar?'.format(eventDescription)})

# run the app
if __name__ == '__main__':
    app.run(debug=True)