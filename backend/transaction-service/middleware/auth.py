from functools import wraps
from flask import request, jsonify
import jwt
import os
from config import Config

# Test user when no valid JWT (dev only) – matches budget-service test user
TEST_USER = {'id': '00000000-0000-0000-0000-000000000001', 'email': 'test@example.com', 'name': 'Test User'}

def authenticate_jwt(f):
    """Decorator to validate JWT tokens; in dev, allow no token and use test user."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        # Allow no token in dev: when FLASK_ENV is not production, or DISABLE_AUTH=1
        env = (os.getenv('FLASK_ENV') or '').lower()
        dev_no_auth = (
            env != 'production'
            or os.getenv('DISABLE_AUTH', '').strip() == '1'
        )

        if not auth_header:
            if dev_no_auth:
                request.user = TEST_USER
                return f(*args, **kwargs)
            return jsonify({'error': 'No authorization header provided'}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            if dev_no_auth:
                request.user = TEST_USER
                return f(*args, **kwargs)
            return jsonify({'error': 'Invalid authorization header format'}), 401

        token = parts[1]
        try:
            decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            request.user = decoded
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            if dev_no_auth:
                request.user = TEST_USER
                return f(*args, **kwargs)
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            if dev_no_auth:
                request.user = TEST_USER
                return f(*args, **kwargs)
            return jsonify({'error': 'Invalid token'}), 403

    return decorated_function
