import requests
import os
from datetime import datetime, timedelta
import logging
from models import Topic

class NewsService:
    def __init__(self):
        self.api_key = os.environ.get('NEWS_API_KEY', 'demo_key')
        self.base_url = 'https://newsapi.org/v2'
        
    def get_articles_by_topic(self, topic_name, keywords=None, limit=5):
        """Fetch articles for a specific topic"""
        try:
            # Use keywords if provided, otherwise use topic name
            query = ' OR '.join(keywords) if keywords else topic_name
            
            # Calculate date range (last 3 days)
            to_date = datetime.now()
            from_date = to_date - timedelta(days=3)
            
            params = {
                'q': query,
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'popularity',
                'pageSize': limit,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(f'{self.base_url}/everything', params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            # Filter and format articles
            formatted_articles = []
            for article in articles:
                if self._is_quality_article(article):
                    formatted_articles.append(self._format_article(article, topic_name))
            
            return formatted_articles[:limit]
            
        except Exception as e:
            logging.error(f"Error fetching articles for topic {topic_name}: {str(e)}")
            return []
    
    def get_curated_articles(self):
        """Get curated articles from different topics"""
        from app import app, db
        
        with app.app_context():
            topics = Topic.query.filter_by(active=True).all()
            
            if not topics:
                # Default topics if none configured
                default_topics = [
                    {'name': 'Technology', 'keywords': ['technology', 'AI', 'software', 'innovation']},
                    {'name': 'Science', 'keywords': ['science', 'research', 'discovery', 'health']},
                    {'name': 'Business', 'keywords': ['business', 'economy', 'finance', 'startup']}
                ]
                
                curated_articles = []
                for topic_data in default_topics:
                    articles = self.get_articles_by_topic(topic_data['name'], topic_data['keywords'], 1)
                    if articles:
                        curated_articles.extend(articles)
                
                return curated_articles[:3]
            
            # Get one article from each topic
            curated_articles = []
            for topic in topics[:3]:  # Limit to 3 topics
                articles = self.get_articles_by_topic(topic.name, topic.keywords, 1)
                if articles:
                    curated_articles.extend(articles)
            
            return curated_articles[:3]
    
    def _is_quality_article(self, article):
        """Filter for quality articles"""
        # Skip articles without proper content
        if not article.get('title') or not article.get('description'):
            return False
        
        # Skip articles that are too short
        if len(article.get('description', '')) < 50:
            return False
        
        # Skip removed articles
        if '[Removed]' in article.get('title', '') or '[Removed]' in article.get('description', ''):
            return False
        
        return True
    
    def _format_article(self, article, topic):
        """Format article data for email template"""
        published_at = article.get('publishedAt', '')
        if published_at:
            try:
                published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                formatted_date = published_date.strftime('%B %d, %Y at %I:%M %p UTC')
            except:
                formatted_date = 'Recently'
        else:
            formatted_date = 'Recently'
        
        return {
            'title': article.get('title', 'No title'),
            'description': article.get('description', 'No description available'),
            'url': article.get('url', '#'),
            'source': article.get('source', {}).get('name', 'Unknown Source'),
            'published_date': formatted_date,
            'topic': topic,
            'image_url': article.get('urlToImage', '')
        }
