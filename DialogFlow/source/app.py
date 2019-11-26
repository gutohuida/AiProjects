from init import app
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from apis.ns_intents import api as Intents

from core.config import MYSQL_CONFIG as SQLCONFIG


api = Api(app, version='1.0', title='G.A.B.I', descripition='End point para Gabi.')
api.add_namespace(Intents, path='/Intents')

if __name__ == '__main__':
    app.run(debug=True)