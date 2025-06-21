from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Subscriber, NewsletterSent, ArtForm
from news_service import NewsService
from email_service import EmailService
import logging

news_service = NewsService()
email_service = EmailService()

@app.route('/')
def index():
    subscribers_count = Subscriber.query.filter_by(active=True).count()
    recent_newsletters = NewsletterSent.query.order_by(NewsletterSent.sent_at.desc()).limit(5).all()
    art_forms = ArtForm.query.filter_by(active=True).all()
    
    return render_template('index.html', 
                         subscribers_count=subscribers_count,
                         recent_newsletters=recent_newsletters,
                         art_forms=art_forms)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    name = request.form.get('name', '')
    selected_art_forms = request.form.getlist('art_forms')
    
    if not email:
        flash('Come on, gorgeous - we need your email to deliver the goods!', 'error')
        return redirect(url_for('index'))
    
    # Check if subscriber already exists
    existing_subscriber = Subscriber.query.filter_by(email=email).first()
    if existing_subscriber:
        existing_subscriber.art_forms = selected_art_forms
        existing_subscriber.active = True
        flash('Look who\'s back for more! Your artistic cravings have been updated.', 'success')
    else:
        subscriber = Subscriber(email=email, name=name, art_forms=selected_art_forms)
        db.session.add(subscriber)
        flash('Welcome to the dark side, culture vulture! Your artistic addiction starts now.', 'success')
    
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
    art_forms = ArtForm.query.all()
    return render_template('settings.html', subscribers=subscribers, art_forms=art_forms)

@app.route('/add_art_form', methods=['POST'])
def add_art_form():
    name = request.form.get('name')
    description = request.form.get('description', '')
    keywords = request.form.get('keywords', '').split(',')
    keywords = [k.strip() for k in keywords if k.strip()]
    
    if not name:
        flash('Art form name is required!', 'error')
        return redirect(url_for('settings'))
    
    art_form = ArtForm(name=name, description=description, keywords=keywords)
    db.session.add(art_form)
    db.session.commit()
    flash('Art form added beautifully!', 'success')
    
    return redirect(url_for('settings'))

@app.route('/delete_art_form/<int:art_form_id>')
def delete_art_form(art_form_id):
    art_form = ArtForm.query.get_or_404(art_form_id)
    art_form.active = False
    db.session.commit()
    flash('Art form removed from collection!', 'info')
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
                subject = f"🔥 Your SevenArts Fix - Artistic Overload Incoming"
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
        flash(f'Artistic bombs dropped to {success_count} hungry culture vultures!', 'success')
        
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
