#!/usr/bin/env python3
"""
Script to create Piscine voting polls
"""

from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define the polls
polls = [
    {
        "title": "⭐ 1. Best Staff Legend",
        "description": "Who made your Piscine experience better simply by being supportive, helpful, and always there when you needed guidance?",
        "options": []  # Add names here or leave empty to add via admin panel
    },
    {
        "title": "🔊 2. Volume Icon",
        "description": "Who could never be ignored? From their contagious laughter to their unforgettable presence, who brought the most energy to the Piscine?",
        "options": []
    },
    {
        "title": "🌞 3. The Ray of Sunshine",
        "description": "Who brightened everyone's day with their kindness, positivity, and uplifting spirit during the Piscine?",
        "options": []
    },
    {
        "title": "🖥️ 4. Dedication Beast",
        "description": "Who lived in front of their screen, stayed late, kept grinding, and never gave up even on the toughest Piscine days?",
        "options": []
    },
    {
        "title": "🤝 5. The Collaboration Champion",
        "description": "Who always had your back during the Piscine? The person who helped, supported, and shared knowledge with everyone around them?",
        "options": []
    }
]

def create_poll(title, description, options):
    """Create a poll with options"""
    try:
        # Create the poll
        poll_response = supabase.table('polls').insert({
            'title': title,
            'description': description,
            'opens_label': 'Opens today',
            'closes_label': 'Closes in 3 days'
        }).execute()
        
        poll_id = poll_response.data[0]['id']
        print(f"✓ Created poll: {title} (ID: {poll_id})")
        
        # Create options if provided
        if options:
            for option_name in options:
                supabase.table('options').insert({
                    'poll_id': poll_id,
                    'name': option_name,
                    'votes': 0
                }).execute()
                print(f"  ✓ Added option: {option_name}")
        else:
            print(f"  ℹ No options provided - add them via admin panel")
        
        return poll_id
    except Exception as e:
        print(f"✗ Error creating poll '{title}': {e}")
        return None

def main():
    print("Creating Piscine voting polls...\n")
    
    for poll in polls:
        create_poll(poll['title'], poll['description'], poll['options'])
        print()
    
    print("Done! All polls created successfully.")
    print("\nNext steps:")
    print("1. Go to http://localhost:5001/admin")
    print("2. Login with admin credentials")
    print("3. Add candidate names (options) to each poll")
    print("4. Students can then vote at http://localhost:5001/")

if __name__ == '__main__':
    main()
