from flask_pymongo import pymongo
from app import mongo

class Organisation:
    def __init__(self, name):
        self.name = name
class Employee:
    def __init__(self, name, role, organisation_id):
        self.name = name
        self.role = role
        self.organisation_id = organisation_id