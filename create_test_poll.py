#!/usr/bin/env python3
"""
Create a sample poll to test full Supabase functionality
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

print("🚀 Creating a test poll...\n")

try:
    # Create a poll
    poll_data = {
        'title': 'Test Poll - Favorite Programming Language',
        'description': 'Which programming language do you prefer?',
        'opens_label': 'Opens today',
        'closes_label': 'Closes in 3 days'
    }
    
    poll_response = supabase.table('polls').insert(poll_data).execute()
    poll_id = poll_response.data[0]['id']
    print(f"✅ Created poll with ID: {poll_id}")
    
    # Add options
    options = [
        {'name': 'Python', 'poll_id': poll_id, 'votes': 0},
        {'name': 'JavaScript', 'poll_id': poll_id, 'votes': 0},
        {'name': 'Go', 'poll_id': poll_id, 'votes': 0}
    ]
    
    supabase.table('options').insert(options).execute()
    print(f"✅ Added 3 options to the poll")
    
    # Read back the poll
    result = supabase.table('polls').select('*, options(*)').eq('id', poll_id).execute()
    poll = result.data[0]
    
    print(f"\n📊 Poll Created Successfully!")
    print(f"   Title: {poll['title']}")
    print(f"   Description: {poll['description']}")
    print(f"   Options: {len(poll['options'])} candidates")
    
    print(f"\n🌐 View it at: http://127.0.0.1:5000")
    print(f"   Admin: http://127.0.0.1:5000/admin")
    
except Exception as e:
    print(f"❌ Error: {e}")
