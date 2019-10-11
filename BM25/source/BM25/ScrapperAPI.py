from flask import Flask
from flask import request
from rank_bm25 import BM25Okapi
from BM25Mongo import BM25Scrapper
import json
from nltk.corpus import stopwords

with open('./config.json') as file:
    config = json.load(file)

scrapper = BM25Scrapper(host=config['host'],port=config['port'],data_base=config['data_base'],collection=config['collection'],stop_words=stopwords.words('portuguese'))
app = Flask(__name__)

@app.route("/postPath", methods=["POST"])
def postPath():
   path = request.args.get('path')
   subject = request.args.get('subject') 
   scrapper.scrap(path,subject)
   return 'Ok'

@app.route("/getRanking", methods=["GET"])
def getRanking():
    key_words = request.args.get("key_words").split(",")
    ndocs = int(request.args.get("ndocs"))
    subject = request.args.get("subject")
    titles = []
    corpus = []

    for documment in scrapper.load_all(subject):
        titles.append(documment['title'])
        corpus.append(documment['tokenizedText'].split(','))

    classifier = BM25Okapi(corpus)

    doc_scores = classifier.get_scores(key_words)
    score_tuple = []

    for pos, score in enumerate(doc_scores):
        score_tuple.append((titles[pos],score))
 
    response = {}
    for tsorted in sorted(score_tuple, key=lambda tup: tup[1], reverse=True)[:ndocs]:
        response[tsorted[0]] = tsorted[1]
    
    return json.dumps(response)
 

@app.route("/")
def wellcome():
    return 'Wellcome!'

if __name__ == '__main__':
    app.run(debug=True)