from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Bill, Payment
from datetime import datetime

bills_bp = Blueprint('bills', __name__)

@bills_bp.route('', methods=['GET'])
@jwt_required()
def get_bills():
    user_id = get_jwt_identity()
    bills = Bill.query.filter_by(user_id=user_id).all()
    
    bills_data = []
    for bill in bills:
        bills_data.append({
            'id': bill.id,
            'name': bill.name,
            'amount': bill.amount,
            'due_date': bill.due_date.isoformat(),
            'category': bill.category,
            'frequency': bill.frequency,
            'is_paid': bill.is_paid,
            'notes': bill.notes,
            'created_at': bill.created_at.isoformat(),
            'reminder_preferences': {
                'enable_whatsapp': bill.enable_whatsapp,
                'enable_call': bill.enable_call,
                'enable_sms': bill.enable_sms,
                'enable_local_notification': bill.enable_local_notification
            }
        })
    
    return jsonify(bills_data), 200

@bills_bp.route('', methods=['POST'])
@jwt_required()
def create_bill():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required = ['name', 'amount', 'due_date', 'category', 'frequency']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Create bill
    bill = Bill(
        user_id=user_id,
        name=data['name'],
        amount=data['amount'],
        due_date=datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')),
        category=data['category'],
        frequency=data['frequency'],
        notes=data.get('notes')
    )
    
    # Set reminder preferences if provided
    if 'reminder_preferences' in data:
        prefs = data['reminder_preferences']
        bill.enable_whatsapp = prefs.get('enable_whatsapp', True)
        bill.enable_call = prefs.get('enable_call', False)
        bill.enable_sms = prefs.get('enable_sms', False)
        bill.enable_local_notification = prefs.get('enable_local_notification', True)
    
    db.session.add(bill)
    db.session.commit()
    
    return jsonify({
        'id': bill.id,
        'name': bill.name,
        'amount': bill.amount,
        'due_date': bill.due_date.isoformat(),
        'category': bill.category,
        'frequency': bill.frequency,
        'is_paid': bill.is_paid,
        'notes': bill.notes,
        'created_at': bill.created_at.isoformat(),
        'reminder_preferences': {
            'enable_whatsapp': bill.enable_whatsapp,
            'enable_call': bill.enable_call,
            'enable_sms': bill.enable_sms,
            'enable_local_notification': bill.enable_local_notification
        }
    }), 201

@bills_bp.route('/<bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(bill_id):
    user_id = get_jwt_identity()
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        bill.name = data['name']
    if 'amount' in data:
        bill.amount = data['amount']
    if 'due_date' in data:
        bill.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
    if 'category' in data:
        bill.category = data['category']
    if 'frequency' in data:
        bill.frequency = data['frequency']
    if 'notes' in data:
        bill.notes = data['notes']
    
    # Update reminder preferences
    if 'reminder_preferences' in data:
        prefs = data['reminder_preferences']
        if 'enable_whatsapp' in prefs:
            bill.enable_whatsapp = prefs['enable_whatsapp']
        if 'enable_call' in prefs:
            bill.enable_call = prefs['enable_call']
        if 'enable_sms' in prefs:
            bill.enable_sms = prefs['enable_sms']
        if 'enable_local_notification' in prefs:
            bill.enable_local_notification = prefs['enable_local_notification']
    
    db.session.commit()
    
    return jsonify({
        'id': bill.id,
        'name': bill.name,
        'amount': bill.amount,
        'due_date': bill.due_date.isoformat(),
        'category': bill.category,
        'frequency': bill.frequency,
        'is_paid': bill.is_paid,
        'notes': bill.notes,
        'created_at': bill.created_at.isoformat()
    }), 200

@bills_bp.route('/<bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    user_id = get_jwt_identity()
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404
    
    db.session.delete(bill)
    db.session.commit()
    
    return '', 204

@bills_bp.route('/<bill_id>/pay', methods=['POST'])
@jwt_required()
def mark_bill_paid(bill_id):
    user_id = get_jwt_identity()
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404
    
    bill.is_paid = True
    
    # Create payment record
    payment = Payment(
        bill_id=bill.id,
        amount=bill.amount,
        payment_method='manual'
    )
    
    db.session.add(payment)
    db.session.commit()
    
    return jsonify({'message': 'Bill marked as paid'}), 200