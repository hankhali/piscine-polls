#!/usr/bin/env python3
"""
Automatic database migration script using Supabase REST API.
This applies the text response support migration directly.
"""

from dotenv import load_dotenv
import os
import sys
import requests

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
    sys.exit(1)

print("🔄 Applying database migration automatically...")
print("=" * 60)

# SQL statements to execute (broken into individual statements)
migrations = [
    {
        "name": "Add poll_type column",
        "sql": "ALTER TABLE polls ADD COLUMN IF NOT EXISTS poll_type VARCHAR(50) DEFAULT 'multiple_choice';"
    },
    {
        "name": "Create text_responses table",
        "sql": """CREATE TABLE IF NOT EXISTS text_responses (
            id BIGSERIAL PRIMARY KEY,
            poll_id BIGINT NOT NULL REFERENCES polls(id) ON DELETE CASCADE,
            username VARCHAR(255) NOT NULL,
            response_text TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(poll_id, username)
        );"""
    },
    {
        "name": "Enable RLS on text_responses",
        "sql": "ALTER TABLE text_responses ENABLE ROW LEVEL SECURITY;"
    },
    {
        "name": "Create read policy for text_responses",
        "sql": """DROP POLICY IF EXISTS "Allow public read access to text_responses" ON text_responses;
        CREATE POLICY "Allow public read access to text_responses" 
        ON text_responses FOR SELECT 
        TO public 
        USING (true);"""
    },
    {
        "name": "Create insert policy for text_responses",
        "sql": """DROP POLICY IF EXISTS "Allow public insert access to text_responses" ON text_responses;
        CREATE POLICY "Allow public insert access to text_responses" 
        ON text_responses FOR INSERT 
        TO public 
        WITH CHECK (true);"""
    },
    {
        "name": "Create update policy for text_responses",
        "sql": """DROP POLICY IF EXISTS "Allow public update access to text_responses" ON text_responses;
        CREATE POLICY "Allow public update access to text_responses" 
        ON text_responses FOR UPDATE 
        TO public 
        USING (true);"""
    },
    {
        "name": "Create delete policy for text_responses",
        "sql": """DROP POLICY IF EXISTS "Allow public delete access to text_responses" ON text_responses;
        CREATE POLICY "Allow public delete access to text_responses" 
        ON text_responses FOR DELETE 
        TO public 
        USING (true);"""
    }
]

# Execute each migration using Supabase REST API
headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

print("\n📦 Executing migrations...\n")

for migration in migrations:
    print(f"⏳ {migration['name']}...", end=' ')
    
    # Use the RPC endpoint to execute SQL
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers=headers,
            json={"query": migration['sql']}
        )
        
        # If RPC doesn't exist, we need to use a different approach
        if response.status_code == 404:
            print(f"⚠️  RPC endpoint not available")
            break
        elif response.status_code in [200, 201, 204]:
            print("✅")
        else:
            print(f"⚠️  Status {response.status_code}")
            print(f"    Response: {response.text[:100]}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("\n🔍 Verifying migration status...")

# Verify the migration by checking if we can access the new schema
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

text_responses_exists = False
poll_type_exists = False

try:
    result = supabase.table('text_responses').select('*').limit(0).execute()
    print("✅ text_responses table exists")
    text_responses_exists = True
except Exception as e:
    print("❌ text_responses table does NOT exist")

try:
    result = supabase.table('polls').select('id, poll_type').limit(1).execute()
    print("✅ polls.poll_type column exists")
    poll_type_exists = True
except Exception as e:
    print("❌ polls.poll_type column does NOT exist")

print("\n" + "=" * 60)

if text_responses_exists and poll_type_exists:
    print("✅ SUCCESS! Migration completed successfully.")
    print("\n📋 Your database now supports:")
    print("   • Multiple choice polls (existing)")
    print("   • Text response polls (new)")
    sys.exit(0)
else:
    print("❌ Migration could not be applied automatically.")
    print("\n📝 Manual steps required:")
    print("   1. Go to: https://supabase.com/dashboard")
    print("   2. Select your project → SQL Editor")
    print("   3. Run the SQL from: add_text_response_support.sql")
    print("   4. Run test_deployment.py again to verify")
    sys.exit(1)
