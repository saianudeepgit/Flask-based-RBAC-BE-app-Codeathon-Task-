from flask import Blueprint, request, jsonify
from flask_pymongo import pymongo
from app import mongo
from models import Organisation, Employee
from auth import generate_token
from rbac import role_required

api = Blueprint('api', __name__)

@api.route('/organisations', methods=['POST'])
@role_required(['Role1', 'Role2'])
def create_organisation():
    # create organisation logic here
    return jsonify({'message': 'Organisation created'}), 201

@api.route('/organisations/<org_id>/employees', methods=['POST'])
@role_required(['Role2', 'Role3'])
def create_employee(org_id):
    # create employee logic here
    return jsonify({'message': 'Employee created'}), 201