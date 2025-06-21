import requests
import os
from datetime import datetime, timedelta
import logging

class NewsService:
    def __init__(self):
        self.api_key = os.environ.get('NEWS_API_KEY', 'demo_key')
        self.base_url = 'https://newsapi.org/v2'
        
    def get_articles_by_art_form(self, art_form_name, keywords=None, limit=5):
        """Fetch articles for a specific art form"""
        try:
            # Use keywords if provided, otherwise use art form name
            query = ' OR '.join(keywords) if keywords else art_form_name
            
            # Remove date restrictions for more interesting, diverse content
            params = {
                'q': query,
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'relevancy',  # Changed to relevancy for better cultural content
                'pageSize': limit * 2  # Get more results to filter better
            }
            
            response = requests.get(f'{self.base_url}/everything', params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            # Filter and format articles
            formatted_articles = []
            for article in articles:
                if self._is_quality_article(article):
                    formatted_articles.append(self._format_article(article, art_form_name))
            
            return formatted_articles[:limit]
            
        except Exception as e:
            logging.error(f"Error fetching articles for art form {art_form_name}: {str(e)}")
            return []
    
    def get_curated_articles(self):
        """Get curated articles from different art forms"""
        from app import app, db
        from models import ArtForm
        
        with app.app_context():
            art_forms = ArtForm.query.filter_by(active=True).all()
            
            if not art_forms:
                # The seven classic art forms if none configured
                default_art_forms = [
                    {'name': 'Architecture', 'keywords': ['architecture', 'building design', 'urban planning', 'architectural']},
                    {'name': 'Sculpture', 'keywords': ['sculpture', 'sculptural', 'installation art', 'public art']},
                    {'name': 'Painting', 'keywords': ['painting', 'visual art', 'contemporary art', 'fine art']},
                    {'name': 'Music', 'keywords': ['music', 'classical music', 'contemporary music', 'composer']},
                    {'name': 'Poetry', 'keywords': ['poetry', 'literature', 'poet', 'literary']},
                    {'name': 'Dance', 'keywords': ['dance', 'ballet', 'contemporary dance', 'choreography']},
                    {'name': 'Theater', 'keywords': ['theater', 'theatre', 'drama', 'performance art']}
                ]
                
                curated_articles = []
                # Select 3 random art forms for variety
                import random
                selected_forms = random.sample(default_art_forms, 3)
                
                for art_form_data in selected_forms:
                    articles = self.get_articles_by_art_form(art_form_data['name'], art_form_data['keywords'], 1)
                    if articles:
                        curated_articles.extend(articles)
                
                return curated_articles[:3]
            
            # Get one article from each art form (randomly select 3 for variety)
            import random
            selected_art_forms = random.sample(list(art_forms), min(3, len(art_forms)))
            
            curated_articles = []
            for art_form in selected_art_forms:
                articles = self.get_articles_by_art_form(art_form.name, art_form.keywords, 1)
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
    
    def _format_article(self, article, art_form):
        """Format article data for email template"""
        published_at = article.get('publishedAt', '')
        if published_at:
            try:
                published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                formatted_date = published_date.strftime('%B %d, %Y')
            except:
                formatted_date = 'Cultural Discovery'
        else:
            formatted_date = 'Cultural Discovery'
        
        return {
            'title': article.get('title', 'No title'),
            'description': article.get('description', 'No description available'),
            'url': article.get('url', '#'),
            'source': article.get('source', {}).get('name', 'Cultural Source'),
            'published_date': formatted_date,
            'art_form': art_form,
            'topic': art_form,  # Keep for backward compatibility
            'image_url': article.get('urlToImage', '')
        }
