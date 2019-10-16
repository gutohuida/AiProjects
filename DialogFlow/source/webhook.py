# import flask dependencies
from flask import Flask, request, make_response, jsonify
from DbConector import DbConector
from datetime import date, datetime
from unidecode import unidecode
import json
import locale

#Horario brasileiro
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

#Read config
with open('./config.json') as file:
    config = json.load(file)

#Instatiate Data base handler
db = DbConector(config["host"],config["port"],config["db_name"],config["collection_name"])    

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'


def EventDate(EventName):
    db = DbConector(config["host"],config["port"],config["db_name"],"Events")
    documment = db.findOne({"Name":unidecode(EventName)})
    date = datetime.strptime(documment["Date"],'%Y-%m-%d')
    return date.strftime('%d de %B'), documment["Time"]

def EventLocation(EventName):
    db = DbConector(config["host"],config["port"],config["db_name"],"Events")
    documment = db.findOne({"Name":unidecode(EventName)})
    return  documment["Location"]    

#main webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req["queryResult"]["intent"]["displayName"]
   
    if intent == "EventDate":
        date, time = EventDate(req["queryResult"]["parameters"]["Events"])
        return {"fulfillmentText":"O próximo {0} acontecerá dia {1} as {2}.".format(req["queryResult"]["parameters"]["Events"],date,time)}

    if intent == "EventLocationDate":
        date, time = EventDate(req["queryResult"]["outputContexts"][1]["parameters"]["Events"])
        return {"fulfillmentText":"Será no dia {0} as {1}. Mais alguma coisa?".format(date,time)}

    if intent == "EventLocation":
        location = EventLocation(req["queryResult"]["parameters"]["Events"])
        return {"fulfillmentText": "O {0} acontecerá no {1}.".format(req["queryResult"]["parameters"]["Events"],location)}

    if intent == "EventDateLocal":
        for value in req["queryResult"]["outputContexts"]:
            if value["name"].endswith("eventdate-followup"):
                event = value["parameters"]["Events"]

        location = EventLocation(event)
        return {"fulfillmentText": "Será no {0}. Mais alguma coisa?".format(location)}

# run the app
if __name__ == '__main__':
    app.run(debug=True)