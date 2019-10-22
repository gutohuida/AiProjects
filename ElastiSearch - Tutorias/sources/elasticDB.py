from elasticsearch import Elasticsearch

class ElasticDB():
    def __init__(self,host,port):
        self.es = Elasticsearch([{'host': host, 'port': port}])
        if self.es.ping():
            print("conectou")

    def index(self,index,doc_type,body):
        res = self.es.index(index=index,doc_type=doc_type,body=body)
        return res


