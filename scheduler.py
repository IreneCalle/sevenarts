from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import atexit
from flask import current_app

def send_scheduled_newsletter():
    """Function to send scheduled cultural digest"""
    try:
        from app import app, db
        from models import Subscriber
        from news_service import NewsService
        from email_service import EmailService
        
        with app.app_context():
            logging.info("Starting scheduled cultural digest send...")
            
            news_service = NewsService()
            email_service = EmailService()
            
            # Get all active subscribers
            subscribers = Subscriber.query.filter_by(active=True).all()
            
            if not subscribers:
                logging.info("No active culture vultures found")
                return
            
            # Get articles for cultural digest
            articles = news_service.get_curated_articles()
            
            if not articles:
                logging.error("No cultural articles found for digest")
                return
            
            success_count = 0
            for subscriber in subscribers:
                try:
                    subject = f"Your SevenArts Cultural Digest - Fresh Discoveries"
                    email_service.send_newsletter(subscriber.email, subject, articles, subscriber.name)
                    success_count += 1
                    
                except Exception as e:
                    logging.error(f"Failed to send cultural digest to {subscriber.email}: {str(e)}")
            
            logging.info(f"Scheduled cultural digest sent to {success_count} art lovers")
            
    except Exception as e:
        logging.error(f"Error in scheduled cultural digest send: {str(e)}")

def start_scheduler():
    """Start the background scheduler"""
    scheduler = BackgroundScheduler()
    
    # Schedule cultural digest to be sent daily at 8:00 AM
    scheduler.add_job(
        func=send_scheduled_newsletter,
        trigger=CronTrigger(hour=8, minute=0),  # 8:00 AM daily
        id='daily_cultural_digest',
        name='Send daily cultural digest',
        replace_existing=True
    )
    
    # For testing, you can also add a job that runs every minute
    # scheduler.add_job(
    #     func=send_scheduled_newsletter,
    #     trigger=CronTrigger(minute='*'),  # Every minute
    #     id='test_cultural_digest',
    #     name='Test cultural digest',
    #     replace_existing=True
    # )
    
    scheduler.start()
    logging.info("SevenArts cultural digest scheduler started")
    
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
