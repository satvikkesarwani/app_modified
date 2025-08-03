import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///bills_reminder.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # API Keys
    BLAND_AI_API_KEY = os.getenv('BLAND_AI_API_KEY')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # AWS S3 (for receipt storage)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', 'bills-reminder-receipts')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # ElevenLabs (alternative voice service)
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'rachel')