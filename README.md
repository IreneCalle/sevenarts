# 🎨 SevenArts - Cultural Newsletter System

A beautiful, modern web application that curates and delivers cultural content about the seven classical arts through personalized email newsletters.

![SevenArts Preview](https://via.placeholder.com/800x400/FF8C42/FFFFFF?text=SevenArts+Cultural+Newsletter)

## ✨ Features

- **Modern Watercolor Design** - Tangerine and lush green aesthetic with floating leaves animation
- **Seven Classical Arts** - Architecture, Sculpture, Painting, Music, Poetry, Dance, Theater
- **Smart Curation** - AI-powered article selection from diverse cultural sources
- **Email Newsletters** - Beautiful HTML emails with cultural discoveries
- **Subscription Management** - Easy signup with art form preferences
- **Automated Delivery** - Daily cultural doses at 8:00 AM
- **Responsive Design** - Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- NewsAPI key
- SMTP email service

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd sevenarts
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   # Required
   NEWS_API_KEY=your_newsapi_key
   DATABASE_URL=your_postgres_url
   SESSION_SECRET=your_secret_key
   
   # Email configuration (choose one)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### NewsAPI Setup
1. Sign up at [newsapi.org](https://newsapi.org)
2. Get your free API key
3. Add `NEWS_API_KEY` to environment variables

### Email Setup
Choose one of these SMTP providers:

#### Gmail (Recommended)
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_16_character_app_password
```

#### SendGrid
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_sendgrid_api_key
```

## 🎨 Design Philosophy

SevenArts embraces a modern watercolor aesthetic with:
- **Typography**: Inter for headings, Plus Jakarta Sans for body text
- **Colors**: Warm tangerine (#FF8C42) and lush forest green (#2D5A3D)
- **Elements**: Organic shapes, soft gradients, glass-morphism effects
- **Animation**: Gentle floating leaves and watercolor-inspired transitions

## 📱 Tech Stack

- **Backend**: Flask, SQLAlchemy, APScheduler
- **Database**: PostgreSQL with automatic migrations
- **Frontend**: Bootstrap 5, Custom CSS with watercolor styling
- **Email**: SMTP with HTML template rendering
- **API**: NewsAPI for content aggregation
- **Deployment**: Gunicorn WSGI server

## 🎭 Art Forms

The system covers seven classical art forms:

1. **Architecture** - Building design and urban planning
2. **Sculpture** - Three-dimensional art and installations
3. **Painting** - Visual art with pigments and brushes
4. **Music** - Organized sound and rhythm
5. **Poetry** - Literary art using language and verse
6. **Dance** - Movement and choreography
7. **Theater** - Live performance and dramatic arts

## 📧 Newsletter Features

- **Personalized Content** - Based on selected art form preferences
- **Quality Curation** - Hand-picked articles from reliable sources
- **Beautiful Design** - Watercolor-styled HTML email templates
- **Mobile Responsive** - Perfect rendering on all email clients
- **Unsubscribe Management** - Easy opt-out with one click

## 🔄 Automated Scheduling

- **Daily Delivery** - Cultural doses sent every morning at 8:00 AM
- **Smart Batching** - Efficient email delivery with error handling
- **Content Rotation** - Fresh articles from different art forms each time
- **Delivery Tracking** - Monitor sent newsletters and engagement

## 🛠️ Development

### Project Structure
```
sevenarts/
├── app.py              # Flask application setup
├── models.py           # Database models
├── routes.py           # Web routes and handlers
├── news_service.py     # NewsAPI integration
├── email_service.py    # SMTP email handling
├── scheduler.py        # Background task management
├── static/
│   └── style.css       # Watercolor styling
├── templates/          # Jinja2 templates
└── instance/           # Database files
```

### Key Components
- **Subscriber Management** - Email collection with preferences
- **Article Curation** - Smart filtering and selection
- **Email Templates** - Beautiful HTML newsletter design
- **Background Scheduler** - Automated delivery system

## 🎨 Customization

The watercolor design system uses CSS custom properties:
```css
:root {
    --tangerine: #FF8C42;
    --lush-green: #2D5A3D;
    --sage-green: #87A96B;
    /* ... more colors */
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support, email ireneccprogramacion@gmail.com or create an issue on GitHub.

---

*"Ready for your next artistic high? We've handpicked irresistible cultural gems that'll make your creative soul purr."* 🎨
