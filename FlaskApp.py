from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'klosdhsdh564sdg456bbs654db64s5h65sh65s44str4h56s165nbs1t5r4tht56hs1th4str6h4str4651st4rhb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MyDatabase'

mongo = PyMongo(app)

def token_required(permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                user_role = data.get('role')
                if user_role not in permissions:
                    return jsonify({'message': 'Unauthorized access!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid!'}), 401
            return func(*args, **kwargs)
        return wrapper
    return decorator

role_permissions = {
    'role1': ['create', 'read'],
    'role2': ['create', 'read', 'update'],
    'role3': ['create', 'read', 'update', 'delete']
}

class Organisation:
    def __init__(self, name):
        self.name = name

class College:
    def __init__(self, name):
        self.name = name

class Employee:
    def __init__(self, name, organisation_id):
        self.name = name
        self.organisation_id = organisation_id

class Book:
    def __init__(self, title, college_id):
        self.title = title
        self.college_id = college_id

@app.route('/create/organisation', methods=['POST'])
@token_required(role_permissions['role1'])
def create_organisation():
    data = request.get_json()
    name = data.get('name')
    organisation = Organisation(name)
    mongo.db.organisations.insert_one({'name': organisation.name})
    return jsonify({'message': 'Organisation created successfully!'})

@app.route('/create/college', methods=['POST'])
@token_required(role_permissions['role2'])
def create_college():
    data = request.get_json()
    name = data.get('name')
    college = College(name)
    mongo.db.colleges.insert_one({'name': college.name})
    return jsonify({'message': 'College created successfully!'})

@app.route('/create/employee', methods=['POST'])
@token_required(role_permissions['role3'])
def create_employee():
    data = request.get_json()
    name = data.get('name')
    organisation_id = data.get('organisation_id')
    employee = Employee(name, organisation_id)
    mongo.db.employees.insert_one({'name': employee.name, 'organisation_id': employee.organisation_id})
    return jsonify({'message': 'Employee created successfully!'})

@app.route('/create/book', methods=['POST'])
@token_required(role_permissions['role3'])
def create_book():
    data = request.get_json()
    title = data.get('title')
    college_id = data.get('college_id')
    book = Book(title, college_id)
    mongo.db.books.insert_one({'title': book.title, 'college_id': book.college_id})
    return jsonify({'message': 'Book created successfully!'})

@app.route('/update/organisation/61e42fd65b290b2973c5c8d1', methods=['PUT'])
@token_required(role_permissions['role2'])
@token_required(role_permissions['role3'])
def update_organisation(organisation_id):
    data = request.get_json()
    new_name = data.get('name')
    mongo.db.organisations.update_one({'_id': organisation_id}, {'$set': {'name': new_name}})
    return jsonify({'message': 'Organisation updated successfully!'})

@app.route('/update/college/61e42fe05b290b2973c5c8d2', methods=['PUT'])
@token_required(role_permissions['role2'])
@token_required(role_permissions['role3'])
def update_college(college_id):
    data = request.get_json()
    new_name = data.get('name')
    mongo.db.colleges.update_one({'_id': college_id}, {'$set': {'name': new_name}})
    return jsonify({'message': 'College updated successfully!'})

@app.route('/update/employee/61e42fe85b290b2973c5c8d3', methods=['PUT'])
@token_required(role_permissions['role3'])
def update_employee(employee_id):
    data = request.get_json()
    new_name = data.get('name')
    new_organisation_id = data.get('organisation_id')
    mongo.db.employees.update_one({'_id': employee_id}, {'$set': {'name': new_name, 'organisation_id': new_organisation_id}})
    return jsonify({'message': 'Employee updated successfully!'})

@app.route('/delete/employee/61e42ff15b290b2973c5c8d4', methods=['DELETE'])
@token_required(role_permissions['role3'])
def delete_employee(employee_id):
    mongo.db.employees.delete_one({'_id': employee_id})
    return jsonify({'message': 'Employee deleted successfully!'})

@app.route('/search/<collection>', methods=['GET'])
@token_required(role_permissions['role1'])  
@token_required(role_permissions['role2'])
@token_required(role_permissions['role3'])
def search(collection):
    query = request.args.get('query')
    result = mongo.db[collection].find({'$text': {'$search': query}})
    return jsonify([item for item in result])

if __name__ == '__main__':
    app.run(debug=True)
