from flask import Flask, jsonify
from flask import request
from rank_bm25 import BM25Okapi
from BM25Mongo import BM25Scrapper
import json
from nltk.corpus import stopwords

with open('./config.json') as file:
    config = json.load(file)

JSON_SORT_KEYS = False

scrapper = BM25Scrapper(host=config['host'],port=config['port'],data_base=config['data_base'],collection=config['collection'],stop_words=stopwords.words('portuguese'))
app = Flask(__name__)

@app.route("/postPath", methods=["POST"])
def postPath():
    path = request.args.get('path')
    subject = request.args.get('subject')
    print('Starting...')
    print() 
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
    
    for tsorted in sorted(score_tuple, key=lambda tup: tup[1], reverse=True): 
    #for tsorted in score_tuple.sort(key=lambda x: x[1]):  
        if tsorted[1] > 0:
            response[tsorted[0]] = str(tsorted[1])
    print(response)
    return jsonify(response)

@app.route("/getRanking2", methods=["GET"])
def getRanking2():
    files = request.get_json(force=True)
    learning_itens = files['itemAprendizagens']
    key_words = files["keywords"]
    subject = files["subject"]
    item_names = []
    titles = []
    corpus = []
    urls = []

    for item in learning_itens:
        if item['sistemaRepositorio']:
            item_names.append({"nome":item['sistemaRepositorio']['nome'],"url":item['sistemaRepositorio']["url"]})

    documments = scrapper.load_list(subject,item_names)

    for documment in documments:
        if documment['document']:
            titles.append(documment['document']['title'])
            urls.append(documment['url'])
            corpus.append(documment['document']['tokenizedText'].split(','))

    classifier = BM25Okapi(corpus)

    doc_scores = classifier.get_scores(key_words)
    print(doc_scores)
    score_tuple = []

    for pos, score in enumerate(doc_scores):
        score_tuple.append((titles[pos],score,urls[pos]))
 
    response = {}
    for tsorted in sorted(score_tuple, key=lambda tup: tup[1], reverse=True):
        if tsorted[1] > 0:
            response[tsorted[0]] = [tsorted[1],tsorted[2]]
       
    
    return json.dumps(response)
    # return "ok"
    

@app.route("/")
def wellcome():
    return 'Wellcome!'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5001)