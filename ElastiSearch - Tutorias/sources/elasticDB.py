from elasticsearch import Elasticsearch
import os
import textract



class ElasticDB():
    def __init__(self,connection):
       # self.es = Elasticsearch(host=host, port=port,http_auth=('kibanaadmin', 'nupedia'))
        self.es = Elasticsearch([connection])
        if not self.es.ping():
            raise Exception("Não conectado")

                

    def index(self,index,doc_type,body):
        res = self.es.index(index=index,doc_type=doc_type,body=body)
        return res

    def scrap(self,path,subject,index,doc_type):
        corpus = {}
        for filename in os.listdir(path):
            #Preenche os dados que seram inseridos no banco        
            corpus['titulo'] = filename
            corpus['texto'] =  textract.process(path+filename, encoding = "utf-8").decode("utf-8")
            corpus['disciplina'] = subject
            res = self.es.index(index=index,doc_type=doc_type,body=corpus)
            corpus = {}
        return res

    def search(self,index,query):
        res = self.es.search(index=index,body=query)
        return res