from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bills = db.relationship('Bill', backref='user', lazy=True, cascade='all, delete-orphan')
    reminder_settings = db.relationship('ReminderSettings', backref='user', uselist=False, cascade='all, delete-orphan')

class Bill(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(20), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Reminder preferences
    enable_whatsapp = db.Column(db.Boolean, default=True)
    enable_call = db.Column(db.Boolean, default=False)
    enable_sms = db.Column(db.Boolean, default=False)
    enable_local_notification = db.Column(db.Boolean, default=True)
    
    payments = db.relationship('Payment', backref='bill', lazy=True, cascade='all, delete-orphan')

class Payment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bill_id = db.Column(db.String(36), db.ForeignKey('bill.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ReminderSettings(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    local_notifications = db.Column(db.Boolean, default=True)
    whatsapp_enabled = db.Column(db.Boolean, default=False)
    call_enabled = db.Column(db.Boolean, default=False)
    sms_enabled = db.Column(db.Boolean, default=False)
    days_before = db.Column(db.Integer, default=3)
    preferred_time = db.Column(db.String(5), default='09:00')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)