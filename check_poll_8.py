#!/usr/bin/env python3
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

print("🔍 Checking Poll ID 8 in Database\n")
print("=" * 60)

# Get poll info
poll_response = supabase.table('polls').select('id, title, poll_type').eq('id', 8).execute()
if poll_response.data:
    poll = poll_response.data[0]
    print(f"\n✅ Poll Found:")
    print(f"   ID: {poll['id']}")
    print(f"   Title: {poll['title']}")
    print(f"   Type: {poll.get('poll_type', 'NULL')}")
else:
    print("❌ Poll 8 not found!")
    exit(1)

# Get options
options_response = supabase.table('options').select('*').eq('poll_id', 8).execute()
print(f"\n📋 Options in Database:")
if options_response.data:
    print(f"   Count: {len(options_response.data)}")
    for opt in options_response.data:
        print(f"   - ID {opt['id']}: {opt['name']} ({opt['votes']} votes)")
else:
    print("   ❌ NO OPTIONS FOUND!")
    print("   This explains why the edit form is empty!")

print("\n" + "=" * 60)

# Now check what the API returns
print("\n🌐 Checking what API returns:\n")
api_response = supabase.table('polls').select('*, options(*)').eq('id', 8).execute()
if api_response.data:
    poll_with_options = api_response.data[0]
    print(f"✅ API Query Result:")
    print(f"   Options count: {len(poll_with_options.get('options', []))}")
    if poll_with_options.get('options'):
        for opt in poll_with_options['options']:
            print(f"   - {opt['name']}")
    else:
        print("   ❌ API returns empty options array!")

print("\n" + "=" * 60)
print("\n💡 Conclusion:")
if not options_response.data:
    print("   The database has NO options for poll 8.")
    print("   When you edit and add options, they're not being saved.")
    print("   Check the Flask terminal for UPDATE debug messages!")
elif not poll_with_options.get('options'):
    print("   Options exist in DB but API doesn't return them.")
    print("   This is a backend API problem!")
else:
    print("   Everything looks OK in the database!")
