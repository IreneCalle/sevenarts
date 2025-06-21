# News Curator - Automated Newsletter System

## Overview

News Curator is a Flask-based web application that automates the creation and distribution of curated newsletters. The system fetches news articles from external APIs, allows users to subscribe with topic preferences, and automatically sends scheduled newsletters via email.

## System Architecture

The application follows a modular Flask architecture with the following key components:

### Backend Architecture
- **Flask Web Framework**: Main application server handling HTTP requests and responses
- **SQLAlchemy ORM**: Database abstraction layer for managing subscribers, newsletters, and topics
- **APScheduler**: Background task scheduler for automated newsletter sending
- **SMTP Integration**: Email delivery system using configurable SMTP servers

### Database Design
- **SQLite/PostgreSQL**: Flexible database backend with environment-based configuration
- **Three main entities**:
  - `Subscriber`: User information, email preferences, and topic subscriptions
  - `NewsletterSent`: Tracking of sent newsletters and delivery status
  - `Topic`: Configurable news categories with keyword filtering

### External Service Integration
- **NewsAPI**: Third-party news aggregation service for article retrieval
- **SMTP Services**: Email delivery through configurable SMTP providers (Gmail by default)

## Key Components

### Core Application (`app.py`)
- Flask application factory pattern
- Database initialization and configuration
- ProxyFix middleware for deployment compatibility
- Environment-based configuration management

### Data Models (`models.py`)
- **Subscriber Model**: Email, name, topic preferences, subscription status
- **NewsletterSent Model**: Newsletter delivery tracking with article content
- **Topic Model**: Dynamic topic management with keyword-based filtering

### News Service (`news_service.py`)
- NewsAPI integration for article fetching
- Topic-based article filtering and curation
- Article quality assessment and formatting
- Date-based article filtering (last 3 days)

### Email Service (`email_service.py`)
- Multi-format email support (HTML and plain text)
- Template-based newsletter generation
- SMTP configuration and delivery
- Subscriber-specific personalization

### Scheduler (`scheduler.py`)
- Background task management using APScheduler
- Configurable newsletter sending schedule
- Error handling and logging for automated tasks
- Application context management for database operations

### Web Interface (`routes.py`)
- Subscription management endpoints
- Topic preference handling
- Newsletter preview functionality
- Administrative settings interface

## Data Flow

1. **Subscription Process**:
   - User submits subscription form with email and topic preferences
   - System validates email and creates/updates subscriber record
   - Topic preferences stored as JSON array in subscriber model

2. **Article Curation**:
   - Scheduler triggers article fetching based on configured intervals
   - News service queries NewsAPI with topic-specific keywords
   - Articles filtered for quality and relevance
   - Curated content prepared for newsletter generation

3. **Newsletter Distribution**:
   - Scheduler initiates newsletter sending process
   - System retrieves active subscribers and their preferences
   - Personalized newsletters generated using HTML templates
   - Emails sent via SMTP with delivery status tracking

## External Dependencies

### Required APIs
- **NewsAPI**: News article aggregation (requires API key)
- **SMTP Server**: Email delivery service (Gmail, SendGrid, etc.)

### Python Packages
- Flask ecosystem: Flask, Flask-SQLAlchemy, Werkzeug
- Scheduling: APScheduler with timezone support
- HTTP clients: Requests for API communication
- Database: SQLAlchemy with PostgreSQL/SQLite support
- Email: Built-in smtplib with MIME support
- Validation: Email-validator for input validation

### Frontend Dependencies
- Bootstrap 5 with dark theme support
- Font Awesome icons for UI enhancement
- Responsive design for mobile compatibility

## Deployment Strategy

### Production Configuration
- **Gunicorn WSGI Server**: Production-ready application server
- **Environment Variables**: Secure configuration management
- **Database Migration**: SQLAlchemy-based schema management
- **Proxy Configuration**: ProxyFix for reverse proxy deployment

### Environment Variables
- `DATABASE_URL`: Database connection string
- `NEWS_API_KEY`: NewsAPI authentication
- `SMTP_*`: Email server configuration
- `SESSION_SECRET`: Flask session security

### Scaling Considerations
- Background scheduler runs as part of main application
- Database connection pooling with automatic recycling
- Stateless design enables horizontal scaling
- External service dependencies may require rate limiting

## Changelog
- June 21, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.