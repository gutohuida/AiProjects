import nltk as nltk
from nltk.corpus import stopwords
import os
import PyPDF2
import textract
import re
import pymongo
from pymongo import MongoClient
from unidecode import unidecode
from pymongo.errors import BulkWriteError



class BM25Scrapper:
    def __init__(self,host=None,port=None,data_base=None,collection=None,stop_words=None,regex=r'[(\n).,?!]'):
        self.host = host
        self.port = port
        self.data_base_name = data_base
        self.collection_name = collection
        self.regex = regex
        self.stop_words = stop_words
        
        #self._start_mongo_db()    
        
    def set_mongo_db(self,data_base):
        if self.client:
            self.data_base = self.client[data_base]
        else:
            raise Exception('001 - Mongo connection not initialized. Please use "set_mongo_connection" to initialize the connection.')
            
    def set_collection(self,collection):
        if self.data_base:
            self.collection = self.data_base[collection]
        else:
            raise Exception('002 - Data Base not defined. Please use "set_mongo_db" to define a Data Base.')    
                    
    def _start_mongo_db(self):
        if self.host and self.port:
            self.set_mongo_connection(self.host,self.port)
            
        if self.data_base_name:
            self.set_mongo_db(self.data_base_name)
            
        if self.collection_name:
            self.set_collection(self.collection_name)
   
    def set_mongo_connection(self,host,port):
        self.client = MongoClient(host,port)
     
    def _load_documments(self,path):
        self.not_found = []
        self.documments = []
        self._start_mongo_db()    
        # for filename in os.listdir(path):
        #     documment = self.collection.find_one({'title': filename})
        #     if not documment:
        #         self.not_found.append(filename)
        #     else:
        #         self.documments.append(documment)
        for filename in os.listdir(path):
            self.not_found.append(filename)
        self.client.close()        

    def load_all(self,key):
        self._start_mongo_db()
        documments = self.collection.find({'disciplina':key})
        self.client.close()
        return documments

    def load_list(self,key,names):
        documments = []
        self._start_mongo_db()
        for name in names:
            documments.append({"document":self.collection.find_one({"$and" : [{'disciplina' : key},{'title':unidecode(re.sub(r'( -* )| |-','_',name["nome"]))}]}),"url":name["url"]})
            
        self.client.close()         
        return(documments)

    def _insert_mongo(self,post):
        if self.collection and post:
            try:
                #result = self.collection.insert_many(post)
                result = self.collection.insert_one(post)
                return result
            except BulkWriteError as bwe:
                return bwe.details
            
                    
    def scrap(self,path,subject):
        self._load_documments(path)
        pdfs = {}
        corpus = {}
        post_file = []
        corpus_aux = []
        for i in range(9):
            for filename in self.not_found:

                print(path+filename)
                pdfs[filename] = textract.process(path+filename, encoding = "utf-8").decode("utf-8")
                
                #Trata o arquivo extraido tokenizando, retirando caracteres especiais e deixando em minusculo o conteudo        
                for word in nltk.word_tokenize(unidecode(re.sub(self.regex,'',pdfs[filename].lower()))):
                    if word not in self.stop_words:
                        corpus_aux.append(word)

                #Preenche os dados que seram inseridos no banco        
                # corpus['title'] = filename
                # corpus['tokenizedText'] = ','.join(corpus_aux)
                # corpus['disciplina'] = subject
                # post_file.append(corpus)
                # corpus = {}
                # corpus_aux = []

                
                post_file.append([','.join(corpus_aux),filename])
                corpus_aux = []
    
        corpus['disciplina'] = subject
        corpus['docs'] = post_file  
        #Insere todos os registros no banco    
        self._insert_mongo(corpus)
        #return post_file + self.documments

      