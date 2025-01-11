from functools import wraps
from flask import request, jsonify
from models.User import User
from .generate_token import decode_token

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
  
        token = request.headers.get('Authorization')
        api_key = request.headers.get("API")

        if not token:
            return jsonify({'error': 'Token is missing!'}), 403
        
        if not api_key:
            return jsonify({'error': 'api_key is missing!'}), 403
        
        
        if api_key != "volvo_ty":
            return jsonify({'error': 'api_key is incorrect!'}), 403
            
        
        
            
        
        
        if token.startswith("Bearer "):
            token = token[7:]  
        else:
            return jsonify({'error': 'Token format is incorrect!'}), 403

        try:
            decoded_data = decode_token(token)  
            user = User.query.filter_by(email=decoded_data['email']).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if 'admin' not in [role.name for role in user.roles]:
                return jsonify({'error': 'Access restricted to admins only'}), 403
            
        except Exception as e:
            return jsonify({'error': 'Invalid token or error occurred'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
