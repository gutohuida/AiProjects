from elasticsearch import Elasticsearch
import os
import textract
from unidecode import unidecode
import re
import nltk as nltk
from nltk.corpus import stopwords



class ElasticDB():
    def __init__(self,connection):
       # self.es = Elasticsearch(host=host, port=port,http_auth=('kibanaadmin', 'nupedia'))
        self.es = Elasticsearch([connection])
        if not self.es.ping():
            raise Exception("Não conectado")

  

    def index(self,index,doc_type,body):
        res = self.es.index(index=index,doc_type=doc_type,body=body)
        return res

    def scrap(self,path,subject,index,doc_type,extract_type='treated'):
        corpus = {}
        corpus_aux = []
        stop_words = stopwords.words('portuguese')
        for filename in os.listdir(path):
            #Preenche os dados que seram inseridos no banco        
            corpus['titulo'] = filename
            if extract_type == 'treated':
                corpus['texto'] =  unidecode(re.sub(r'[(\n)(\r).,?!]','',(textract.process(path+filename, encoding = "utf-8").decode("utf-8").lower())))
            elif extract_type == 'pure':
                corpus['texto'] =  textract.process(path+filename, encoding = "utf-8").decode("utf-8")
            elif extract_type == 'tokenized':
                for word in nltk.word_tokenize(unidecode(re.sub(r'[(\n)(\r).,?!]','',textract.process(path+filename, encoding = "utf-8").decode("utf-8").lower()))):
                    if word not in stop_words:
                        corpus_aux.append(word)
                corpus['texto'] =  ' '.join(corpus_aux)

            corpus['disciplina'] = subject
            res = self.es.index(index=index,doc_type=doc_type,body=corpus)
            corpus = {}
        return res
       

    def search_query(self,index,query):
        #Vai receber um conjunto de disciplina no qual ele pode procurar e as palavras chaves que eu vou procurar.
        print(query)
        res = self.es.search(index=index,body=query)
        return res

    def search(self,indexes,keywords):
        #Vai receber um conjunto de disciplina no qual ele pode procurar e as palavras chaves que eu vou procurar.
        query = {
            "_source": [
                "titulo"
            ],
            "size": 1000,
            "query": {
                "match": {
                    "texto": {
                        "query": " ".join(keywords),
                        "operator": "or"
                    }
                }
            }
        }

        res = self.es.search(index=indexes,body=query)
        return res    