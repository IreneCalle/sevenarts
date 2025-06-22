# SMTP Email Setup for SevenArts

## Option 1: Gmail (Recommended - Free & Easy)

### Steps:
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
3. **Add these to Replit Secrets**:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_16_character_app_password
   ```

## Option 2: SendGrid (Professional)

### Steps:
1. **Sign up** at sendgrid.com (free tier: 100 emails/day)
2. **Create API Key** in Settings → API Keys
3. **Add these to Replit Secrets**:
   ```
   SMTP_SERVER=smtp.sendgrid.net
   SMTP_PORT=587
   SMTP_USERNAME=apikey
   SMTP_PASSWORD=your_sendgrid_api_key
   ```

## Option 3: Outlook/Hotmail

### Steps:
1. **Enable 2FA** and generate app password
2. **Add these to Replit Secrets**:
   ```
   SMTP_SERVER=smtp-mail.outlook.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@outlook.com
   SMTP_PASSWORD=your_app_password
   ```

## How to Add Secrets in Replit:
1. Click the lock icon 🔒 in the left sidebar
2. Click "Add new secret"
3. Add each variable name and value
4. Restart your app

## Test Your Setup:
Once configured, try:
1. Subscribe with your email
2. Click "Drop Cultural Bombs Now"
3. Check your inbox for the newsletter