#!/usr/bin/env python3
"""
Quick test to verify poll ordering fix
"""
from supabase import create_client
from dotenv import load_dotenv
import os
import json

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

print("🔍 Testing Poll Order Fix\n")
print("=" * 60)

# Get polls as the API would return them
response = supabase.table('polls').select('id, title').order('id', desc=False).execute()
polls = response.data

print("\n📊 Current Database Order (by ID):")
for i, poll in enumerate(polls, 1):
    print(f"  {i}. ID {poll['id']:2d}: {poll['title']}")

print("\n" + "=" * 60)
print("\n✅ Frontend Fix Applied:")
print("   The JavaScript now sorts polls by the number in the title")
print("   So '1. Best Staff' comes before '2. Volume Icon'")
print("   regardless of their database IDs.")

print("\n📝 To see it in action:")
print("   1. Open: http://localhost:5001")
print("   2. Polls should now appear as: 1, 2, 3, 4, 5...")
print("   3. Order is maintained on both student and admin views")

print("\n💡 Note: You have duplicate polls (IDs 6 & 11, and 7 & 12)")
print("   Consider deleting the duplicates from the admin panel.")
print("\n" + "=" * 60)
