from functools import wraps
from flask import request, jsonify
from auth import decode_token

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
            user_id = decode_token(token)
            # Check user role and permissions
            # Implement your RBAC logic here
            return func(*args, **kwargs)
        return wrapper
    return decorator