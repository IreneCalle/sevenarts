# SevenArts Setup Guide

## Required API Keys & Environment Variables

To make SevenArts fully functional, you need to set up the following environment variables:

### 1. NewsAPI Key (Required for fetching cultural articles)
- Go to https://newsapi.org
- Sign up for a free account
- Get your API key from the dashboard
- Set environment variable: `NEWS_API_KEY=your_actual_key_here`

### 2. Email Configuration (Required for sending newsletters)
Choose one of these options:

#### Option A: Gmail SMTP
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password
```
*Note: Use an App Password, not your regular Gmail password*

#### Option B: SendGrid
```
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_sendgrid_api_key
```

### 3. Database (Auto-configured)
- PostgreSQL is automatically set up in Replit
- `DATABASE_URL` is already configured

### 4. Security (Auto-configured)
- `SESSION_SECRET` is automatically set by Replit

## Setup Steps

1. **Get NewsAPI Key**
   - Visit newsapi.org and sign up
   - Copy your API key
   - Add `NEWS_API_KEY` to your Replit Secrets

2. **Configure Email**
   - Choose Gmail or SendGrid
   - Add the appropriate SMTP variables to Replit Secrets

3. **Test the Application**
   - Subscribe with your email
   - Check the "Preview Newsletter" to see sample content
   - Send a test newsletter to verify email delivery

## Testing Without API Keys

The app will run without API keys but with limited functionality:
- Newsletter preview will show "Artistic Drought Alert" 
- No emails will be sent
- Subscription still works (data is saved)

## Current Status

✅ Database: Ready (PostgreSQL auto-configured)
✅ Web Interface: Fully functional
✅ Subscription System: Working
❌ News Fetching: Needs `NEWS_API_KEY`
❌ Email Sending: Needs SMTP configuration

## Art Forms Pre-loaded

The seven classical art forms are automatically set up:
- Architecture
- Sculpture  
- Painting
- Music
- Poetry
- Dance
- Theater

Each has specific keywords for filtering cultural articles.