from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, ReminderSettings, Bill
from reminder_service import generate_reminder_message, send_whatsapp_reminder, send_voice_reminder
from elevenlabs_service import generate_voice_audio
from datetime import datetime

reminders_bp = Blueprint('reminders', __name__)

@reminders_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_reminder_settings():
    user_id = get_jwt_identity()
    settings = ReminderSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        # Create default settings
        settings = ReminderSettings(user_id=user_id)
        db.session.add(settings)
        db.session.commit()
    
    return jsonify({
        'local_notifications': settings.local_notifications,
        'whatsapp_enabled': settings.whatsapp_enabled,
        'call_enabled': settings.call_enabled,
        'sms_enabled': settings.sms_enabled,
        'days_before': settings.days_before,
        'preferred_time': settings.preferred_time
    }), 200

@reminders_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_reminder_settings():
    user_id = get_jwt_identity()
    settings = ReminderSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        settings = ReminderSettings(user_id=user_id)
        db.session.add(settings)
    
    data = request.get_json()
    
    if 'local_notifications' in data:
        settings.local_notifications = data['local_notifications']
    if 'whatsapp_enabled' in data:
        settings.whatsapp_enabled = data['whatsapp_enabled']
    if 'call_enabled' in data:
        settings.call_enabled = data['call_enabled']
    if 'sms_enabled' in data:
        settings.sms_enabled = data['sms_enabled']
    if 'days_before' in data:
        settings.days_before = data['days_before']
    if 'preferred_time' in data:
        settings.preferred_time = data['preferred_time']
    
    db.session.commit()
    
    return jsonify({'message': 'Settings updated successfully'}), 200

@reminders_bp.route('/test', methods=['POST'])
@jwt_required()
def test_reminder():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.phone_number:
        return jsonify({'message': 'Phone number required for reminders'}), 400
    
    data = request.get_json()
    reminder_type = data.get('type')
    
    if reminder_type not in ['whatsapp', 'call', 'elevenlabs']:
        return jsonify({'message': 'Invalid reminder type'}), 400
    
    # Create test bill data
    test_bill_data = {
        'name': 'Test Bill',
        'amount': 1000,
        'due_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Generate message
    message = generate_reminder_message(user.name, test_bill_data)
    
    # Send reminder based on type
    if reminder_type == 'whatsapp':
        result = send_whatsapp_reminder(user.phone_number, message)
    elif reminder_type == 'call':
        result = send_voice_reminder(user.phone_number, message)
    elif reminder_type == 'elevenlabs':
        # Generate audio file using ElevenLabs
        audio_result = generate_voice_audio(message)
        if audio_result['success']:
            result = {'success': True, 'message': 'Audio generated', 'audio_path': audio_result['audio_path']}
        else:
            result = audio_result
    
    if result.get('success'):
        return jsonify({
            'status': 'success',
            'message': f'Test reminder sent via {reminder_type}',
            'details': result
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': f'Failed to send reminder via {reminder_type}',
            'details': result
        }), 500

@reminders_bp.route('/send', methods=['POST'])
@jwt_required()
def send_reminder():
    """Send reminder for a specific bill"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    bill_id = data.get('bill_id')
    reminder_type = data.get('type')
    
    if not bill_id or not reminder_type:
        return jsonify({'message': 'Missing bill_id or type'}), 400
    
    # Get bill and user
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404
    
    user = User.query.get(user_id)
    if not user.phone_number:
        return jsonify({'message': 'Phone number required'}), 400
    
    # Prepare bill data
    bill_data = {
        'name': bill.name,
        'amount': bill.amount,
        'due_date': bill.due_date.strftime('%Y-%m-%d')
    }
    
    # Generate and send reminder
    message = generate_reminder_message(user.name, bill_data)
    
    if reminder_type == 'whatsapp' and bill.enable_whatsapp:
        result = send_whatsapp_reminder(user.phone_number, message)
    elif reminder_type == 'call' and bill.enable_call:
        result = send_voice_reminder(user.phone_number, message)
    else:
        return jsonify({'message': 'Reminder type not enabled for this bill'}), 400
    
    if result.get('success'):
        return jsonify({
            'status': 'success',
            'message': f'Reminder sent via {reminder_type}'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to send reminder',
            'details': result
        }), 500