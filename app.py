import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///newsletter.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    
    # Drop all tables and recreate with new schema
    db.drop_all()
    db.create_all()
    
    # Add default seven art forms
    from models import ArtForm
    default_art_forms = [
        {
            'name': 'Architecture', 
            'keywords': ['architecture', 'building design', 'urban planning', 'architectural'],
            'description': 'The art of designing and constructing buildings'
        },
        {
            'name': 'Sculpture', 
            'keywords': ['sculpture', 'sculptural', 'installation art', 'public art'],
            'description': 'Three-dimensional art forms and installations'
        },
        {
            'name': 'Painting', 
            'keywords': ['painting', 'visual art', 'contemporary art', 'fine art'],
            'description': 'Visual art created with pigments and brushes'
        },
        {
            'name': 'Music', 
            'keywords': ['music', 'classical music', 'contemporary music', 'composer'],
            'description': 'The art of organized sound and rhythm'
        },
        {
            'name': 'Poetry', 
            'keywords': ['poetry', 'literature', 'poet', 'literary'],
            'description': 'Literary art using language and verse'
        },
        {
            'name': 'Dance', 
            'keywords': ['dance', 'ballet', 'contemporary dance', 'choreography'],
            'description': 'Movement and choreography as artistic expression'
        },
        {
            'name': 'Theater', 
            'keywords': ['theater', 'theatre', 'drama', 'performance art'],
            'description': 'Live performance and dramatic arts'
        }
    ]
    
    # Check if art forms already exist
    if ArtForm.query.count() == 0:
        for art_form_data in default_art_forms:
            art_form = ArtForm(
                name=art_form_data['name'],
                keywords=art_form_data['keywords'],
                description=art_form_data['description']
            )
            db.session.add(art_form)
        db.session.commit()
        logging.info("Added default seven art forms to database")

# Import routes
import routes
