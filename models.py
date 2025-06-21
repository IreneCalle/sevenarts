from app import db
from datetime import datetime
from sqlalchemy import Text, JSON

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    topics = db.Column(JSON, default=list)  # List of preferred topics
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Subscriber {self.email}>'

class NewsletterSent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), nullable=False)
    articles = db.Column(JSON)  # Store the articles that were sent
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    subject = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')  # pending, sent, failed
    
    subscriber = db.relationship('Subscriber', backref=db.backref('newsletters', lazy=True))
    
    def __repr__(self):
        return f'<NewsletterSent {self.id} for {self.subscriber.email}>'

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    keywords = db.Column(JSON, default=list)  # Keywords for filtering articles
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Topic {self.name}>'
