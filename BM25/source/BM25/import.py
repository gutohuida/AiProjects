##Endpoint novo
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
        item_names.append({"nome":item['sistemaRepositorio']['nome'],"url":item['sistemaRepositorio']["url"]})

    documments = scrapper.load_list(subject,item_names)

    for documment in documments:
        if documment['document']:
            titles.append(documment['document']['title'])
            urls.append(documment['url'])
            corpus.append(documment['document']['tokenizedText'].split(','))

    classifier = BM25Okapi(corpus)

    doc_scores = classifier.get_scores(key_words)
    score_tuple = []

    for pos, score in enumerate(doc_scores):
        score_tuple.append((titles[pos],score,urls[pos]))
 
    response = {}
    for tsorted in sorted(score_tuple, key=lambda tup: tup[1], reverse=True):
        if tsorted[1] > 0:
            response[tsorted[0]] = [tsorted[1],tsorted[2]]
       
    
    return json.dumps(response)



##Vai na classe BM25Scrapper
     def load_list(self,key,names):
        documments = []
        self._start_mongo_db()
        for name in names:
            documments.append({"document":self.collection.find_one({"$and" : [{'disciplina' : key},{'title':unidecode(re.sub(r'( -* )| |-','_',name["nome"]))}]}),"url":name["url"]})
            
        self.client.close()         
        return(documments)