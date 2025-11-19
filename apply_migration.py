#!/usr/bin/env python3
"""
Direct database migration using psycopg2 or alternative methods.
This applies the text response support migration.
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

print("🔄 Checking and applying database migration...")
print("=" * 60)

# First, check current state
print("\n🔍 Checking current database schema...\n")

text_responses_exists = False
poll_type_exists = False

try:
    result = supabase.table('text_responses').select('*').limit(0).execute()
    print("✅ text_responses table already exists")
    text_responses_exists = True
except Exception as e:
    print("❌ text_responses table does NOT exist")

try:
    result = supabase.table('polls').select('id, poll_type').limit(1).execute()
    print("✅ polls.poll_type column already exists")
    poll_type_exists = True
except Exception as e:
    print("❌ polls.poll_type column does NOT exist")

if text_responses_exists and poll_type_exists:
    print("\n" + "=" * 60)
    print("✅ Migration already applied! Database is ready.")
    print("\n📋 Your database supports:")
    print("   • Multiple choice polls")
    print("   • Text response polls")
    sys.exit(0)

# If not applied, try to apply using PostgREST admin endpoint
print("\n" + "=" * 60)
print("⚠️  Migration needed. Attempting to apply...\n")

# Read SQL file
with open('add_text_response_support.sql', 'r') as f:
    sql_content = f.read()

print("📋 SQL to execute:")
print("-" * 60)
print(sql_content)
print("-" * 60)

# Try different methods to apply the migration
print("\n🔧 Trying to apply migration...\n")

# Method 1: Try using Supabase's query method (if available)
try:
    # Some Supabase clients support raw SQL execution
    # This might work with service_role key
    import requests
    
    # Try the SQL endpoint
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    # Split SQL into individual statements
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    success_count = 0
    for i, statement in enumerate(statements, 1):
        if not statement:
            continue
            
        print(f"   Executing statement {i}/{len(statements)}...", end=' ')
        
        # Try executing via SQL API (if enabled)
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec",
            headers=headers,
            json={"query": statement}
        )
        
        if response.status_code in [200, 201, 204]:
            print("✅")
            success_count += 1
        else:
            print(f"⚠️  ({response.status_code})")
            
    if success_count > 0:
        print(f"\n✅ Applied {success_count}/{len(statements)} statements")
    else:
        print("\n⚠️  Automatic execution not available")
        
except Exception as e:
    print(f"⚠️  Could not execute automatically: {str(e)}")

# Verify again
print("\n🔍 Verifying migration status...\n")

try:
    result = supabase.table('text_responses').select('*').limit(0).execute()
    print("✅ text_responses table exists")
    text_responses_exists = True
except Exception as e:
    print("❌ text_responses table does NOT exist")
    text_responses_exists = False

try:
    result = supabase.table('polls').select('id, poll_type').limit(1).execute()
    print("✅ polls.poll_type column exists")
    poll_type_exists = True
except Exception as e:
    print("❌ polls.poll_type column does NOT exist")
    poll_type_exists = False

print("\n" + "=" * 60)

if text_responses_exists and poll_type_exists:
    print("✅ SUCCESS! Migration completed.")
    sys.exit(0)
else:
    print("⚠️  Automatic migration not supported by your Supabase setup.")
    print("\n📝 MANUAL STEPS REQUIRED:")
    print("\n   1. Open: https://supabase.com/dashboard")
    print("   2. Select your project")
    print("   3. Go to: SQL Editor")
    print("   4. Click: New Query")
    print("   5. Paste the SQL shown above")
    print("   6. Click: Run")
    print("\n   Then run this script again to verify.")
    print("\n💡 The SQL is also saved in: add_text_response_support.sql")
    sys.exit(1)
