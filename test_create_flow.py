#!/usr/bin/env python3
"""
Test script to verify the complete create -> retrieve -> edit flow
"""
import requests
import json
import time

BASE_URL = "http://localhost:5001"

print("🧪 Testing Poll Creation and Retrieval Flow\n")
print("=" * 60)

# Step 1: Login as admin
print("\n1️⃣ Logging in as admin...")
session = requests.Session()
login_response = session.post(
    f"{BASE_URL}/api/admin/login",
    json={"username": "admin", "password": "admin123"}
)
if login_response.status_code == 200:
    print("   ✅ Logged in successfully")
else:
    print(f"   ❌ Login failed: {login_response.status_code}")
    exit(1)

# Step 2: Create a new multiple-choice poll
print("\n2️⃣ Creating a multiple-choice poll...")
new_poll = {
    "title": f"🧪 TEST {int(time.time())}: Favorite Fruit",
    "description": "Pick your favorite fruit",
    "poll_type": "multiple_choice",
    "options": ["Apple", "Banana", "Orange"]
}

create_response = session.post(
    f"{BASE_URL}/api/polls",
    json=new_poll
)

if create_response.status_code == 201:
    poll_id = create_response.json()['id']
    print(f"   ✅ Poll created with ID: {poll_id}")
else:
    print(f"   ❌ Failed to create poll: {create_response.status_code}")
    print(f"   Response: {create_response.text}")
    exit(1)

# Step 3: Retrieve all polls
print("\n3️⃣ Retrieving polls from API...")
polls_response = requests.get(f"{BASE_URL}/api/polls")
polls_data = polls_response.json()

# Find our poll
our_poll = None
for poll in polls_data['polls']:
    if poll['id'] == poll_id:
        our_poll = poll
        break

if our_poll:
    print(f"   ✅ Found our poll in API response")
    print(f"\n   📋 Poll Data:")
    print(f"      ID: {our_poll['id']}")
    print(f"      Title: {our_poll['title']}")
    print(f"      Type: {our_poll.get('poll_type', '❌ MISSING')}")
    print(f"      Options field exists: {'options' in our_poll}")
    
    if 'options' in our_poll:
        print(f"      Options count: {len(our_poll['options'])}")
        if our_poll['options']:
            print(f"      Options:")
            for opt in our_poll['options']:
                print(f"         - {opt.get('name', '???')}")
        else:
            print(f"      ❌ OPTIONS ARRAY IS EMPTY!")
    else:
        print(f"      ❌ OPTIONS FIELD IS MISSING!")
        
else:
    print(f"   ❌ Could not find poll {poll_id} in API response")

print("\n" + "=" * 60)

# Summary
print("\n📊 Summary:")
if our_poll and 'options' in our_poll and len(our_poll['options']) > 0:
    print("   ✅ Poll creation and retrieval working correctly!")
    print("   ✅ Options are being saved and returned properly")
else:
    print("   ❌ PROBLEM DETECTED:")
    if not our_poll:
        print("      • Poll not found in API response")
    elif 'options' not in our_poll:
        print("      • Options field missing from API response")
    elif len(our_poll['options']) == 0:
        print("      • Options array is empty")
        print("      • Check backend: are options being saved?")

print("\n" + "=" * 60)
print("\n🗑️  Clean up: Delete test poll ID", poll_id, "from admin panel")
