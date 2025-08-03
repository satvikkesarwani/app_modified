from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, ReminderSettings
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required = ['email', 'password', 'name', 'phone_number']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 409
    
    # Hash password
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user = User(
        email=data['email'],
        password_hash=password_hash.decode('utf-8'),
        name=data['name'],
        phone_number=data['phone_number']
    )
    
    # Create default reminder settings
    reminder_settings = ReminderSettings(user_id=user.id)
    
    db.session.add(user)
    db.session.add(reminder_settings)
    db.session.commit()
    
    # Create token
    token = create_access_token(identity=user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = create_access_token(identity=user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'phone_number': user.phone_number
        }
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'phone_number' in data:
        user.phone_number = data['phone_number']
    
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'phone_number': user.phone_number
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT tokens are stateless, so we just return success
    return jsonify({'message': 'Logged out successfully'}), 200