# import flask dependencies
from flask import Flask, request, make_response, jsonify
from DbConector import DbConector


# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'


def EventDate(EventName):
    return 'OK'

#main webhook
@app.route('/webhook2', methods=['GET', 'POST'])
def webhook2():
    req = request.get_json(force=True)
    intent = req["intent"]["displayName"] 

    if intent == "EventDate":
        date, time = EventDate(req["queryResult"]["Events"])
        return {"filfillmentText":"O próximo {0} acontecerá dia {1} as {2}".format(req["queryResult"]["Events"],date,time)}



# run the app
if __name__ == '__main__':
    app.run(debug=True)