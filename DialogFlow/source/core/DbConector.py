import pymongo
from pymongo import MongoClient
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from init import app


from core.config import MYSQL_CONFIG as SQLCONFIG

# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{password}@{ip}/{db}'.format(user=SQLCONFIG["user"],password=SQLCONFIG["password"],ip=SQLCONFIG["host"],db=SQLCONFIG["db"])
db = SQLAlchemy(app)


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

    def findAll(self,query):
        self.initDB()    
        documments = self.collection.find(query)
        self.closeDB()
        return documments

class Evento(db.Model):
    evento_id = db.Column(db.Integer, primary_key=True)
    evento_nome = db.Column(db.String(255))
    evento_local = db.Column(db.String(255))
    evento_data = db.Column(db.DateTime)
    evento_desc = db.Column(db.String(3000))
    evento_inc_date = db.Column(db.DateTime)
    evento_alter_date = db.Column(db.DateTime)
    evento_inc_usu_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))
    evento_alt_usu_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))
    gbg_id = db.Column(db.Integer, db.ForeignKey('gbg.gbg_id'))

    def __repr__(self):
        return '<Evento %r>' % self.evento_nome

    #usuarioinc = db.relationship('usuario', backref=db.backref('evento',lazy=True))



