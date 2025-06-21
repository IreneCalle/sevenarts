from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import atexit
from flask import current_app

def send_scheduled_newsletter():
    """Function to send scheduled newsletters"""
    try:
        from app import app, db
        from models import Subscriber
        from news_service import NewsService
        from email_service import EmailService
        
        with app.app_context():
            logging.info("Starting scheduled newsletter send...")
            
            news_service = NewsService()
            email_service = EmailService()
            
            # Get all active subscribers
            subscribers = Subscriber.query.filter_by(active=True).all()
            
            if not subscribers:
                logging.info("No active subscribers found")
                return
            
            # Get articles for newsletter
            articles = news_service.get_curated_articles()
            
            if not articles:
                logging.error("No articles found for newsletter")
                return
            
            success_count = 0
            for subscriber in subscribers:
                try:
                    subject = f"Your Daily News Digest - {articles[0]['published_date']}"
                    email_service.send_newsletter(subscriber.email, subject, articles, subscriber.name)
                    success_count += 1
                    
                except Exception as e:
                    logging.error(f"Failed to send newsletter to {subscriber.email}: {str(e)}")
            
            logging.info(f"Scheduled newsletter sent to {success_count} subscribers")
            
    except Exception as e:
        logging.error(f"Error in scheduled newsletter send: {str(e)}")

def start_scheduler():
    """Start the background scheduler"""
    scheduler = BackgroundScheduler()
    
    # Schedule newsletter to be sent daily at 8:00 AM
    scheduler.add_job(
        func=send_scheduled_newsletter,
        trigger=CronTrigger(hour=8, minute=0),  # 8:00 AM daily
        id='daily_newsletter',
        name='Send daily newsletter',
        replace_existing=True
    )
    
    # For testing, you can also add a job that runs every minute
    # scheduler.add_job(
    #     func=send_scheduled_newsletter,
    #     trigger=CronTrigger(minute='*'),  # Every minute
    #     id='test_newsletter',
    #     name='Test newsletter',
    #     replace_existing=True
    # )
    
    scheduler.start()
    logging.info("Newsletter scheduler started")
    
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
