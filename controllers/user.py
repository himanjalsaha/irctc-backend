from models.User import User , Role
from utils.db import db
from utils.generate_token import generate_token
from flask import request , jsonify
from werkzeug.security import generate_password_hash , check_password_hash 
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_name = data.get('role', 'user')  # Default role is 'user'

        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return jsonify({'error': f"Role '{role_name}' does not exist"}), 400

        hashed_password = generate_password_hash(password)

        user = User(username=username, email=email, password=hashed_password)
        user.roles.append(role)  # Assign role to the user

        db.session.add(user)
        db.session.commit()

        return jsonify({'status': 'User created successfully!', 'status code': 200, 'user_id': user.id}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
    
def login():
    try:
    
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

 
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400


        user = User.query.filter_by(email=email).first()
        

       
        if not user:
            return jsonify({'error': 'Invalid email '}), 401


        if not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid  password'}), 401
        roles = [role.name for role in user.roles]

        token  = generate_token(user.username ,  email , roles)

        return jsonify({'message': 'Login successful', 'token': token , "roles":roles }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500