import nltk as nltk
from nltk.corpus import stopwords
import os
import PyPDF2
import re
import pymongo
from pymongo import MongoClient
from unidecode import unidecode
from pymongo.errors import BulkWriteError



class BM25Scrapper:
    def __init__(self,host=None,port=None,data_base=None,collection=None,stop_words=None,regex=r'[(\n)\.*]'):
        self.host = host
        self.port = port
        self.data_base_name = data_base
        self.collection_name = collection
        self.regex = regex
        self.stop_words = stop_words
        
        self._start_mongo_db()    
        
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
        for filename in os.listdir(path):
            documment = self.collection.find_one({'title': filename})
            if not documment:
                self.not_found.append(filename)
            else:
                self.documments.append(documment)
    
    
    def _insert_mongo(self,post):
        if self.collection and post:
            try:
                result = self.collection.insert_many(post)
            except BulkWriteError as bwe:
                return bwe.details
            
                    
    def scrap(self,path):
        self._load_documments(path)
        pdfs = {}
        corpus = {}
        post_file = []
        corpus_aux = []
        for filename in self.not_found:
            pdfFileObj = open(path+filename, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                pdfs[filename] = (pageObj.extractText() if i == 0 else pdfs[filename]+' '+pageObj.extractText())
            for word in nltk.word_tokenize(unidecode(re.sub(self.regex,'',pdfs[filename].lower()))):
                if word not in self.stop_words:
                    corpus_aux.append(word)
            corpus['title'] = filename
            corpus['tokenizedText'] = corpus_aux
            corpus['disciplina'] = 'logica de programacao'
            post_file.append(corpus)
            corpus = {}
            corpus_aux = []
        self._insert_mongo(post_file)
        return post_file + self.documments

      