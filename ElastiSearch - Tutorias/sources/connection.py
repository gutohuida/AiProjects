# import flask dependencies
from flask import Flask, request, make_response, jsonify
from elasticDB import ElasticDB

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/insertDocument')
def insert():
    req = request.get_json(force=True)
    index = req["index"]
    doc_type = req["doc_type"]
    es = ElasticDB('localhost',9200)
    for arq in req['files']:
        es.index(index,doc_type,arq)
    #keywords = req["keywords"]
    return "ok"



# run the app
if __name__ == '__main__':
    app.run(debug=True)    