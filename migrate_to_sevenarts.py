#!/usr/bin/env python3
"""
Migration script to convert from News Curator to SevenArts
- Renames tables from Topic to ArtForm
- Changes subscriber.topics to subscriber.art_forms
- Updates existing data
"""

import sqlite3
import os
import json

def migrate_database():
    """Migrate the existing database to SevenArts schema"""
    db_path = 'newsletter.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("No existing database found. New schema will be created automatically.")
        return
    
    print("Starting migration to SevenArts...")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if migration already done
        cursor.execute("PRAGMA table_info(subscriber)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'art_forms' in columns:
            print("Migration already completed.")
            return
        
        print("Creating new schema...")
        
        # Create new ArtForm table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS art_form (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                keywords TEXT,
                active BOOLEAN DEFAULT 1,
                description VARCHAR(200)
            )
        """)
        
        # Migrate data from topic to art_form if topic table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='topic'")
        if cursor.fetchone():
            print("Migrating topics to art forms...")
            cursor.execute("SELECT id, name, keywords, active FROM topic")
            topics = cursor.fetchall()
            
            for topic_id, name, keywords_json, active in topics:
                keywords = json.loads(keywords_json) if keywords_json else []
                cursor.execute("""
                    INSERT OR IGNORE INTO art_form (name, keywords, active, description)
                    VALUES (?, ?, ?, ?)
                """, (name, json.dumps(keywords), active, f"Migrated from {name}"))
        
        # Add default seven art forms if none exist
        cursor.execute("SELECT COUNT(*) FROM art_form")
        if cursor.fetchone()[0] == 0:
            print("Adding default seven art forms...")
            default_art_forms = [
                ('Architecture', ['architecture', 'building design', 'urban planning', 'architectural'], 'The art of designing and constructing buildings'),
                ('Sculpture', ['sculpture', 'sculptural', 'installation art', 'public art'], 'Three-dimensional art forms and installations'),
                ('Painting', ['painting', 'visual art', 'contemporary art', 'fine art'], 'Visual art created with pigments and brushes'),
                ('Music', ['music', 'classical music', 'contemporary music', 'composer'], 'The art of organized sound and rhythm'),
                ('Poetry', ['poetry', 'literature', 'poet', 'literary'], 'Literary art using language and verse'),
                ('Dance', ['dance', 'ballet', 'contemporary dance', 'choreography'], 'Movement and choreography as artistic expression'),
                ('Theater', ['theater', 'theatre', 'drama', 'performance art'], 'Live performance and dramatic arts')
            ]
            
            for name, keywords, description in default_art_forms:
                cursor.execute("""
                    INSERT INTO art_form (name, keywords, active, description)
                    VALUES (?, ?, 1, ?)
                """, (name, json.dumps(keywords), description))
        
        # Create backup of subscriber table
        cursor.execute("ALTER TABLE subscriber RENAME TO subscriber_backup")
        
        # Create new subscriber table with art_forms column
        cursor.execute("""
            CREATE TABLE subscriber (
                id INTEGER PRIMARY KEY,
                email VARCHAR(120) NOT NULL UNIQUE,
                name VARCHAR(100),
                art_forms TEXT DEFAULT '[]',
                active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Migrate subscriber data
        print("Migrating subscriber data...")
        cursor.execute("SELECT id, email, name, topics, active, created_at FROM subscriber_backup")
        subscribers = cursor.fetchall()
        
        for sub_id, email, name, topics_json, active, created_at in subscribers:
            # Convert topics to art_forms
            if topics_json:
                try:
                    topics = json.loads(topics_json)
                    art_forms = topics  # For now, keep the same values
                except:
                    art_forms = []
            else:
                art_forms = []
            
            cursor.execute("""
                INSERT INTO subscriber (id, email, name, art_forms, active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (sub_id, email, name, json.dumps(art_forms), active, created_at))
        
        # Drop old tables
        cursor.execute("DROP TABLE IF EXISTS topic")
        cursor.execute("DROP TABLE subscriber_backup")
        
        # Commit changes
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()