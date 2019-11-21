# -*- coding: utf-8 -*-

# imports
from flask import Flask, request, make_response, jsonify
from flask_restplus import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from datetime import date, datetime
from unidecode import unidecode
import json
import locale
import logging

from events import EventDate, EventDescription, EventLocation, Events
from config import MONGO_CONFIG as CONFIG
from config import MYSQL_CONFIG as SQLCONFIG

#Horario brasileiro
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

# initialize the flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{password}@{ip}/{db}'.format(user=SQLCONFIG["user"],password=SQLCONFIG["password"],ip=SQLCONFIG["host"],db=SQLCONFIG["db"])
db = SQLAlchemy(app)
api = Api(app=app)


@api.route('/sql/select')
class SQL(Resource):
    def post(self):
        return 'ok'

#main webhook
@api.route('/webhook')
class Webhook(Resource):
    def post(self):
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