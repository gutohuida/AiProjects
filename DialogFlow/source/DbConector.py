import pymongo
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy as sql



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

# class evento(db.Model):
#     evento_id = sql.Column(sql.Integer, primary_key=True)
#     evento_nome = sql.Column(sql.String(255))
#     evento_local = sql.Column(sql.String(255))
#     evento_data = sql.Column(sql.DateTime)
#     evento_desc = sql.Column(sql.String(3000))
#     evento_inc_date = sql.Column(sql.DateTime)
#     evento_alter_date = sql.Column(sql.DateTime)
#     evento_inc_usu_id = sql.Column(sql.Integer, sql.ForeingKey('usuario.usuario_id'))
#     evento_alt_usu_id = sql.Column(sql.Integer, sql.ForeingKey('usuario.usuario_id'))
#     gbg_id = sql.Column(sql.Integer, sql.ForeingKey('gbg.gbg_id'))

#     def __repr__(self):
#         return '<Evento %r>' % self.evento_nome

#     #usuarioinc = sql.relationship('usuario', backref=sql.backref('evento',lazy=True))



