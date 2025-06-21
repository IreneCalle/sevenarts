# SevenArts - Cultural Newsletter System

## Overview

SevenArts is a Flask-based web application that curates and distributes cultural content about the seven classical arts. The system fetches articles about art forms from external APIs, allows users to subscribe with art form preferences, and automatically sends scheduled cultural digests via email with fresh discoveries every time.

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
  - `Subscriber`: User information, email preferences, and art form subscriptions
  - `NewsletterSent`: Tracking of sent cultural digests and delivery status
  - `ArtForm`: Configurable art categories with keyword filtering and descriptions

### External Service Integration
- **NewsAPI**: Third-party content aggregation service for cultural article retrieval
- **SMTP Services**: Email delivery through configurable SMTP providers (Gmail by default)

## Key Components

### Core Application (`app.py`)
- Flask application factory pattern
- Database initialization and configuration
- ProxyFix middleware for deployment compatibility
- Environment-based configuration management

### Data Models (`models.py`)
- **Subscriber Model**: Email, name, art form preferences, subscription status
- **NewsletterSent Model**: Cultural digest delivery tracking with article content
- **ArtForm Model**: Dynamic art form management with keyword-based filtering and descriptions

### News Service (`news_service.py`)
- NewsAPI integration for cultural article fetching
- Art form-based article filtering and curation
- Article quality assessment and formatting
- Relevancy-based filtering for diverse, interesting content (no date restrictions)

### Email Service (`email_service.py`)
- Multi-format email support (HTML and plain text)
- Template-based cultural digest generation
- SMTP configuration and delivery
- Subscriber-specific personalization with cultural theme

### Scheduler (`scheduler.py`)
- Background task management using APScheduler
- Configurable cultural digest sending schedule
- Error handling and logging for automated tasks
- Application context management for database operations

### Web Interface (`routes.py`)
- Subscription management endpoints
- Art form preference handling
- Cultural digest preview functionality
- Administrative settings interface

## Data Flow

1. **Subscription Process**:
   - User submits subscription form with email and art form preferences
   - System validates email and creates/updates subscriber record
   - Art form preferences stored as JSON array in subscriber model

2. **Article Curation**:
   - Scheduler triggers article fetching based on configured intervals
   - News service queries NewsAPI with art form-specific keywords
   - Articles filtered for quality and cultural relevance
   - Random selection of 3 art forms ensures variety in each digest

3. **Cultural Digest Distribution**:
   - Scheduler initiates cultural digest sending process
   - System retrieves active subscribers and their preferences
   - Personalized cultural digests generated using HTML templates
   - Emails sent via SMTP with delivery status tracking

## External Dependencies

### Required APIs
- **NewsAPI**: Cultural content aggregation (requires API key)
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
- `NEWS_API_KEY`: NewsAPI authentication for cultural content
- `SMTP_*`: Email server configuration
- `SESSION_SECRET`: Flask session security

### Scaling Considerations
- Background scheduler runs as part of main application
- Database connection pooling with automatic recycling
- Stateless design enables horizontal scaling
- External service dependencies may require rate limiting

## Changelog
- June 21, 2025. Initial setup as News Curator
- June 21, 2025. Transformed to SevenArts cultural newsletter system:
  - Renamed application from News Curator to SevenArts
  - Changed focus from general news to seven classical arts
  - Updated database schema: topics → art_forms
  - Modified content curation to focus on cultural articles
  - Added art form descriptions and cultural theming
  - Updated UI with cultural messaging and "culture vulture" theme
  - Removed date restrictions for more diverse, interesting content
  - Added random selection of 3 art forms per digest for variety

## User Preferences

Preferred communication style: Simple, everyday language with cultural flair ("Hi culture vulture! Lovely to see you again").