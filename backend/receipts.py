from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from aws_service import upload_receipt_to_s3, get_receipt_url
from models import db, Bill
import json

receipts_bp = Blueprint('receipts', __name__)

@receipts_bp.route('/scan-receipt', methods=['POST'])
@jwt_required()
def scan_receipt():
    """Upload and process receipt using AWS S3"""
    user_id = get_jwt_identity()
    
    if 'receipt' not in request.files:
        return jsonify({'message': 'No receipt file provided'}), 400
    
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    # Upload to S3
    result = upload_receipt_to_s3(file, user_id)
    
    if not result['success']:
        return jsonify({'message': 'Failed to upload receipt', 'error': result.get('error')}), 500
    
    # Mock OCR processing (in real app, you'd use AWS Textract or similar)
    # For now, return a sample bill structure
    mock_bill_data = {
        'id': None,
        'name': 'Scanned Bill',
        'amount': 0.0,
        'due_date': None,
        'category': 'other',
        'frequency': 'once',
        'is_paid': False,
        'notes': f"Receipt uploaded: {result['filename']}",
        'receipt_url': result['url']
    }
    
    return jsonify(mock_bill_data), 200

@receipts_bp.route('/<bill_id>/receipt', methods=['POST'])
@jwt_required()
def upload_bill_receipt(bill_id):
    """Upload receipt for existing bill"""
    user_id = get_jwt_identity()
    
    # Verify bill ownership
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404
    
    if 'receipt' not in request.files:
        return jsonify({'message': 'No receipt file provided'}), 400
    
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    # Upload to S3
    result = upload_receipt_to_s3(file, user_id)
    
    if not result['success']:
        return jsonify({'message': 'Failed to upload receipt'}), 500
    
    # Update bill notes with receipt info
    notes_data = json.loads(bill.notes or '{}')
    notes_data['receipt_filename'] = result['filename']
    bill.notes = json.dumps(notes_data)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Receipt uploaded successfully',
        'receipt_url': result['url']
    }), 200

@receipts_bp.route('/<bill_id>/receipt', methods=['GET'])
@jwt_required()
def get_bill_receipt(bill_id):
    """Get receipt URL for a bill"""
    user_id = get_jwt_identity()
    
    # Verify bill ownership
    bill = Bill.query.filter_by(id=bill_id, user_id=user_id).first()
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404
    
    # Get receipt filename from notes
    try:
        notes_data = json.loads(bill.notes or '{}')
        receipt_filename = notes_data.get('receipt_filename')
        
        if not receipt_filename:
            return jsonify({'message': 'No receipt found for this bill'}), 404
        
        # Get presigned URL
        result = get_receipt_url(receipt_filename)
        
        if result['success']:
            return jsonify({'receipt_url': result['url']}), 200
        else:
            return jsonify({'message': 'Failed to get receipt URL'}), 500
            
    except:
        return jsonify({'message': 'No receipt found for this bill'}), 404