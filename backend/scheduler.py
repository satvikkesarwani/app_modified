from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from models import db, Bill, User, ReminderSettings
from reminder_service import generate_reminder_message, send_whatsapp_reminder, send_voice_reminder
import pytz

scheduler = BackgroundScheduler()

def check_and_send_reminders():
    """Check for bills due soon and send reminders"""
    with db.app.app_context():
        # Get all users with phone numbers
        users = User.query.filter(User.phone_number.isnot(None)).all()
        
        for user in users:
            # Get user's reminder settings
            settings = ReminderSettings.query.filter_by(user_id=user.id).first()
            if not settings:
                continue
            
            # Check if it's the preferred time
            current_time = datetime.now().strftime('%H:%M')
            if current_time != settings.preferred_time:
                continue
            
            # Get unpaid bills due within reminder window
            reminder_date = datetime.now() + timedelta(days=settings.days_before)
            bills_due = Bill.query.filter(
                Bill.user_id == user.id,
                Bill.is_paid == False,
                Bill.due_date <= reminder_date,
                Bill.due_date >= datetime.now()
            ).all()
            
            for bill in bills_due:
                # Prepare bill data
                bill_data = {
                    'name': bill.name,
                    'amount': bill.amount,
                    'due_date': bill.due_date.strftime('%Y-%m-%d')
                }
                
                # Generate message
                message = generate_reminder_message(user.name, bill_data)
                
                # Send reminders based on preferences
                if settings.whatsapp_enabled and bill.enable_whatsapp:
                    send_whatsapp_reminder(user.phone_number, message)
                
                if settings.call_enabled and bill.enable_call:
                    send_voice_reminder(user.phone_number, message)

def check_overdue_bills():
    """Check for overdue bills and send alerts"""
    with db.app.app_context():
        # Get all overdue bills
        overdue_bills = Bill.query.filter(
            Bill.is_paid == False,
            Bill.due_date < datetime.now()
        ).all()
        
        for bill in overdue_bills:
            user = User.query.get(bill.user_id)
            if not user or not user.phone_number:
                continue
            
            # Calculate days overdue
            days_overdue = (datetime.now() - bill.due_date).days
            
            # Only send daily reminders for first 7 days
            if days_overdue <= 7:
                bill_data = {
                    'name': bill.name,
                    'amount': bill.amount,
                    'due_date': bill.due_date.strftime('%Y-%m-%d'),
                    'days_overdue': days_overdue
                }
                
                # Generate overdue message
                message = f"URGENT: Your {bill.name} payment of ₹{bill.amount} is {days_overdue} days overdue. Please pay immediately to avoid late fees."
                
                # Send via WhatsApp if enabled
                if bill.enable_whatsapp:
                    send_whatsapp_reminder(user.phone_number, message)

def start_scheduler(app):
    """Start the background scheduler"""
    scheduler.add_job(
        func=check_and_send_reminders,
        trigger="cron",
        minute="*",  # Check every minute
        id='reminder_checker',
        replace_existing=True
    )
    
    scheduler.add_job(
        func=check_overdue_bills,
        trigger="cron",
        hour=10,  # Check daily at 10 AM
        minute=0,
        id='overdue_checker',
        replace_existing=True
    )
    
    scheduler.start()