from flask import Flask
from flask_pymongo import pymongo
from config import MONGO_URI

app = Flask(__name__)
app.config.from_pyfile('config.py')

mongo = pymongo.MongoClient(MONGO_URI)
db = mongo.get_default_database()

from app import routes
app.register_blueprint(routes.api)