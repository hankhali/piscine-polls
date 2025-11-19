#!/usr/bin/env python3
"""
Script to automatically apply database migrations to Supabase.
This script applies the text response support migration.
"""

from supabase import create_client
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔄 Starting database migration...")
print("=" * 60)

# Read the SQL migration file
with open('add_text_response_support.sql', 'r') as f:
    sql_content = f.read()

print("\n📋 Migration SQL to be applied:")
print("-" * 60)
print(sql_content)
print("-" * 60)

print("\n⚠️  IMPORTANT: This migration needs to be applied manually.")
print("\nPlease follow these steps:")
print("\n1. Go to your Supabase Dashboard")
print("2. Navigate to: SQL Editor")
print("3. Create a new query")
print("4. Copy and paste the SQL shown above")
print("5. Click 'Run' to execute")
print("\nOR use the Supabase API if you have direct database access.")
print("\n" + "=" * 60)

# Let's try to verify if the migration has been applied
print("\n🔍 Checking current database schema...")

try:
    # Try to query text_responses table
    result = supabase.table('text_responses').select('*').limit(0).execute()
    print("✅ text_responses table exists")
    text_responses_exists = True
except Exception as e:
    print("❌ text_responses table does NOT exist")
    print(f"   Error: {str(e)}")
    text_responses_exists = False

try:
    # Try to query polls with poll_type column
    result = supabase.table('polls').select('id, poll_type').limit(1).execute()
    print("✅ polls.poll_type column exists")
    poll_type_exists = True
except Exception as e:
    print("❌ polls.poll_type column does NOT exist")
    print(f"   Error: {str(e)}")
    poll_type_exists = False

print("\n" + "=" * 60)

if text_responses_exists and poll_type_exists:
    print("✅ Migration already applied! Database is ready.")
    sys.exit(0)
else:
    print("❌ Migration NOT yet applied. Please run the SQL manually.")
    print("\n📝 Quick Steps:")
    print("   1. Copy the SQL from above")
    print("   2. Go to: https://supabase.com/dashboard")
    print("   3. Select your project → SQL Editor")
    print("   4. Paste and run the SQL")
    print("   5. Run this script again to verify")
    sys.exit(1)
