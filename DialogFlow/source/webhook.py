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

#main webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req["queryResult"]["intent"]["displayName"]

    if intent == "EventDate":
        date, time = EventDate(req["queryResult"]["parameters"]["Events"])
        return {"fulfillmentText":"O próximo {0} acontecerá dia {1} as {2}. Posso ajudar com mais alguma coisa?".format(req["queryResult"]["parameters"]["Events"],date,time)}



# run the app
if __name__ == '__main__':
    app.run(debug=True)