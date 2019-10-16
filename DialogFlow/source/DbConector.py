import pymongo
from pymongo import MongoClient



class DbConector():
    def __init__(self,host,port,db_name,collection_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name

    def initDB(self):
        if self.host and self.port:
            self.client = MongoClient(self.host,self.port)    
        else:
            raise Exception('Host or port missing. Please verify the config.json file.')

        if self.db_name:
            self.db = self.client[self.db_name]
        else:
            raise Exception('Data base name missing. Please verify the config.json file.')    
            
        if self.collection_name:    
            self.collection = self.db[self.collection_name]    
        else:
            raise Exception('Collection name missing. Please verify the config.json file.')        

    def closeDB(self):
        self.client.close()

    def findOne(self,query):
        self.initDB()
        documment = self.collection.find_one(query)   
        self.closeDB()
        return documment

