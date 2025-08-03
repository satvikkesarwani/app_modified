from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth_bp
from bills import bills_bp
from reminders import reminders_bp
from receipts import receipts_bp
from scheduler import start_scheduler
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(bills_bp, url_prefix='/api/bills')
    app.register_blueprint(reminders_bp, url_prefix='/api/reminders')
    app.register_blueprint(receipts_bp, url_prefix='/api/bills')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Bills Reminder API is running'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create tables
    with app.app_context():
        db.create_all()
        
    # Start scheduler
    start_scheduler(app)
    
    # Run app
    app.run(debug=True, port=5000)