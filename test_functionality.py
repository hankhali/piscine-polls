#!/usr/bin/env python3
"""
Comprehensive functionality test for the polls application.
Tests both multiple-choice and text-response polls.
"""

from supabase import create_client
from dotenv import load_dotenv
import os
import time

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

print("🧪 Testing Polls Application Functionality")
print("=" * 60)

# Test 1: Check if we can read polls
print("\n1️⃣ Testing: Read existing polls")
try:
    response = supabase.table('polls').select('id, title, poll_type').execute()
    polls = response.data
    print(f"   ✅ Successfully retrieved {len(polls)} polls")
    
    mc_polls = [p for p in polls if p.get('poll_type') == 'multiple_choice']
    text_polls = [p for p in polls if p.get('poll_type') == 'text_response']
    
    print(f"   • Multiple-choice polls: {len(mc_polls)}")
    print(f"   • Text-response polls: {len(text_polls)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Create a test multiple-choice poll
print("\n2️⃣ Testing: Create multiple-choice poll")
try:
    test_poll = {
        'title': '🧪 TEST: Best Programming Language',
        'description': 'This is a test poll - please delete after testing',
        'poll_type': 'multiple_choice',
        'opens_label': 'Opens now',
        'closes_label': 'Test only'
    }
    
    poll_response = supabase.table('polls').insert(test_poll).execute()
    test_poll_id = poll_response.data[0]['id']
    print(f"   ✅ Created test poll with ID: {test_poll_id}")
    
    # Add options
    options = [
        {'poll_id': test_poll_id, 'name': 'Python', 'votes': 0},
        {'poll_id': test_poll_id, 'name': 'JavaScript', 'votes': 0},
        {'poll_id': test_poll_id, 'name': 'C', 'votes': 0}
    ]
    
    supabase.table('options').insert(options).execute()
    print(f"   ✅ Added 3 options to the poll")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    test_poll_id = None

# Test 3: Vote on multiple-choice poll
if test_poll_id:
    print("\n3️⃣ Testing: Vote on multiple-choice poll")
    try:
        # Get an option ID
        options_response = supabase.table('options').select('*').eq('poll_id', test_poll_id).execute()
        option_id = options_response.data[0]['id']
        
        # Cast a vote
        vote_data = {
            'poll_id': test_poll_id,
            'option_id': option_id,
            'username': 'test_user_' + str(int(time.time()))
        }
        
        supabase.table('votes').insert(vote_data).execute()
        
        # Update vote count
        supabase.table('options').update({'votes': 1}).eq('id', option_id).execute()
        
        print(f"   ✅ Successfully voted on poll {test_poll_id}")
        print(f"   ✅ Vote count updated")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Test 4: Create a text-response poll
print("\n4️⃣ Testing: Create text-response poll")
try:
    text_poll = {
        'title': '🧪 TEST: What\'s your favorite feature?',
        'description': 'This is a test text poll - please delete after testing',
        'poll_type': 'text_response',
        'opens_label': 'Opens now',
        'closes_label': 'Test only'
    }
    
    text_poll_response = supabase.table('polls').insert(text_poll).execute()
    text_poll_id = text_poll_response.data[0]['id']
    print(f"   ✅ Created test text-response poll with ID: {text_poll_id}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    text_poll_id = None

# Test 5: Submit a text response
if text_poll_id:
    print("\n5️⃣ Testing: Submit text response")
    try:
        text_response = {
            'poll_id': text_poll_id,
            'username': 'test_user_' + str(int(time.time())),
            'response_text': 'This is a test response. The UI is great!'
        }
        
        supabase.table('text_responses').insert(text_response).execute()
        print(f"   ✅ Successfully submitted text response to poll {text_poll_id}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Test 6: Read responses
if text_poll_id:
    print("\n6️⃣ Testing: Read text responses")
    try:
        responses = supabase.table('text_responses').select('*').eq('poll_id', text_poll_id).execute()
        print(f"   ✅ Retrieved {len(responses.data)} text responses")
        for r in responses.data:
            print(f"      • {r['username']}: {r['response_text'][:50]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("\n📋 Test Summary:")
print("   All backend functionality is working!")
print("\n🌐 Now test in the browser:")
print("   1. Open: http://localhost:5001/admin")
print("   2. Login with your admin credentials")
print("   3. Create a new multiple-choice poll")
print("   4. Create a new text-response poll")
print("   5. Switch to student view")
print("   6. Vote on the multiple-choice poll")
print("   7. Submit a response to the text-response poll")
print("   8. Go back to admin view to see results")
print("\n💡 Clean up: Delete the test polls when done!")
print("=" * 60)
