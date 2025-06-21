from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Subscriber, NewsletterSent, Topic
from news_service import NewsService
from email_service import EmailService
import logging

news_service = NewsService()
email_service = EmailService()

@app.route('/')
def index():
    subscribers_count = Subscriber.query.filter_by(active=True).count()
    recent_newsletters = NewsletterSent.query.order_by(NewsletterSent.sent_at.desc()).limit(5).all()
    topics = Topic.query.filter_by(active=True).all()
    
    return render_template('index.html', 
                         subscribers_count=subscribers_count,
                         recent_newsletters=recent_newsletters,
                         topics=topics)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    name = request.form.get('name', '')
    selected_topics = request.form.getlist('topics')
    
    if not email:
        flash('Email is required!', 'error')
        return redirect(url_for('index'))
    
    # Check if subscriber already exists
    existing_subscriber = Subscriber.query.filter_by(email=email).first()
    if existing_subscriber:
        existing_subscriber.topics = selected_topics
        existing_subscriber.active = True
        flash('Subscription updated successfully!', 'success')
    else:
        subscriber = Subscriber(email=email, name=name, topics=selected_topics)
        db.session.add(subscriber)
        flash('Subscribed successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/unsubscribe/<email>')
def unsubscribe(email):
    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber:
        subscriber.active = False
        db.session.commit()
        flash('Unsubscribed successfully!', 'info')
    else:
        flash('Email not found!', 'error')
    
    return redirect(url_for('index'))

@app.route('/settings')
def settings():
    subscribers = Subscriber.query.filter_by(active=True).all()
    topics = Topic.query.all()
    return render_template('settings.html', subscribers=subscribers, topics=topics)

@app.route('/add_topic', methods=['POST'])
def add_topic():
    name = request.form.get('name')
    keywords = request.form.get('keywords', '').split(',')
    keywords = [k.strip() for k in keywords if k.strip()]
    
    if not name:
        flash('Topic name is required!', 'error')
        return redirect(url_for('settings'))
    
    topic = Topic(name=name, keywords=keywords)
    db.session.add(topic)
    db.session.commit()
    flash('Topic added successfully!', 'success')
    
    return redirect(url_for('settings'))

@app.route('/delete_topic/<int:topic_id>')
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    topic.active = False
    db.session.commit()
    flash('Topic deleted successfully!', 'info')
    return redirect(url_for('settings'))

@app.route('/send_newsletter', methods=['POST'])
def send_newsletter():
    try:
        # Get all active subscribers
        subscribers = Subscriber.query.filter_by(active=True).all()
        
        if not subscribers:
            flash('No active subscribers found!', 'warning')
            return redirect(url_for('index'))
        
        # Get articles for newsletter
        articles = news_service.get_curated_articles()
        
        if not articles:
            flash('No articles found for newsletter!', 'error')
            return redirect(url_for('index'))
        
        success_count = 0
        for subscriber in subscribers:
            try:
                # Send email
                subject = f"Your Daily News Digest - {articles[0]['published_date']}"
                email_service.send_newsletter(subscriber.email, subject, articles, subscriber.name)
                
                # Record the sent newsletter
                newsletter = NewsletterSent(
                    subscriber_id=subscriber.id,
                    articles=articles,
                    subject=subject,
                    status='sent'
                )
                db.session.add(newsletter)
                success_count += 1
                
            except Exception as e:
                logging.error(f"Failed to send newsletter to {subscriber.email}: {str(e)}")
                newsletter = NewsletterSent(
                    subscriber_id=subscriber.id,
                    articles=articles,
                    subject=subject,
                    status='failed'
                )
                db.session.add(newsletter)
        
        db.session.commit()
        flash(f'Newsletter sent to {success_count} subscribers!', 'success')
        
    except Exception as e:
        logging.error(f"Error sending newsletter: {str(e)}")
        flash(f'Error sending newsletter: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/preview_newsletter')
def preview_newsletter():
    try:
        articles = news_service.get_curated_articles()
        return render_template('newsletter.html', articles=articles)
    except Exception as e:
        logging.error(f"Error fetching articles: {str(e)}")
        flash(f'Error fetching articles: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/test_news')
def test_news():
    try:
        articles = news_service.get_curated_articles()
        return jsonify({"success": True, "articles": articles})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
