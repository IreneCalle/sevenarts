import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
import logging

class EmailService:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME', 'your-email@gmail.com')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', 'your-app-password')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username)
        self.from_name = os.environ.get('FROM_NAME', 'News Curator')
    
    def send_newsletter(self, to_email, subject, articles, subscriber_name=None):
        """Send newsletter email to a subscriber"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Generate HTML content
            html_content = render_template('email_template.html', 
                                         articles=articles, 
                                         subscriber_name=subscriber_name,
                                         unsubscribe_url=f"http://localhost:5000/unsubscribe/{to_email}")
            
            # Generate plain text content
            text_content = self._generate_text_content(articles, subscriber_name, to_email)
            
            # Create MIMEText objects
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            # Add parts to message
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logging.info(f"Newsletter sent successfully to {to_email}")
            
        except Exception as e:
            logging.error(f"Failed to send newsletter to {to_email}: {str(e)}")
            raise e
    
    def _generate_text_content(self, articles, subscriber_name, email):
        """Generate plain text version of the newsletter"""
        greeting = f"Hello {subscriber_name}!\n\n" if subscriber_name else "Hello!\n\n"
        
        content = greeting
        content += "Here's your curated news digest:\n\n"
        
        for i, article in enumerate(articles, 1):
            content += f"{i}. {article['title']}\n"
            content += f"   Topic: {article['topic']}\n"
            content += f"   Source: {article['source']}\n"
            content += f"   Published: {article['published_date']}\n"
            content += f"   {article['description']}\n"
            content += f"   Read more: {article['url']}\n\n"
        
        content += "---\n"
        content += f"To unsubscribe, visit: http://localhost:5000/unsubscribe/{email}\n"
        content += "Thanks for reading!\n"
        
        return content
    
    def test_connection(self):
        """Test SMTP connection"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
            return True
        except Exception as e:
            logging.error(f"SMTP connection test failed: {str(e)}")
            return False
