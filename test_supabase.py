#!/usr/bin/env python3
"""
Test script to verify Supabase connection and table setup
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

print("🔍 Testing Supabase Connection...\n")
print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_KEY[:20]}...{SUPABASE_KEY[-10:]}\n")

try:
    # Initialize Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client created successfully!\n")
    
    # Test 1: Check if we can read from polls table
    print("📋 Test 1: Reading polls table...")
    response = supabase.table('polls').select('*').execute()
    print(f"✅ Successfully read polls table!")
    print(f"   Found {len(response.data)} polls\n")
    
    # Test 2: Check if we can read from options table
    print("📋 Test 2: Reading options table...")
    response = supabase.table('options').select('*').execute()
    print(f"✅ Successfully read options table!")
    print(f"   Found {len(response.data)} options\n")
    
    # Test 3: Check if we can read from votes table
    print("📋 Test 3: Reading votes table...")
    response = supabase.table('votes').select('*').execute()
    print(f"✅ Successfully read votes table!")
    print(f"   Found {len(response.data)} votes\n")
    
    print("🎉 All tests passed! Supabase is working correctly!")
    print("\n💡 Your database is ready to use!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️  Possible issues:")
    print("   1. Tables not created - Run the SQL from supabase_schema.sql")
    print("   2. Wrong credentials in .env file")
    print("   3. Network connection issue")
