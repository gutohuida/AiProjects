# import flask dependencies
from flask import Flask, request, make_response, jsonify
from elasticDB import ElasticDB
import json

#Read config
with open('./config.json') as file:
    config = json.load(file)

#Start ElasticDB
es = ElasticDB(config["connection"])

# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/scrap')
def insert():
    #Get json from the body
    req = request.get_json(force=True)
    #Get variables, the information needed, from json
    path = req['path']
    subject = req['subject']
    index = req['index']
    doc_type = req['doc_type']
    #Scrap the documments into Elastic
    es.scrap(path,subject,index,doc_type)
    return 'ok'


@app.route('/searchFiles')   
def search():
    #Get json from the body
    req = request.get_json(force=True)
    #Get variables, the information needed, from json
    index = req['index']
    query = req['query']
    #Search in the index
    res = es.search(index,query)
    return jsonify(res['hits']['hits'])

# run the app
if __name__ == '__main__':
    app.run(debug=True)    