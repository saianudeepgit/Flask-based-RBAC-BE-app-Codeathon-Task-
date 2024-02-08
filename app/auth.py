import jwt
from flask import request, jsonify
from config import SECRET_KEY

def generate_token(user_id):
    token = jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Token is expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'