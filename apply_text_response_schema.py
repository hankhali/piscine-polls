#!/usr/bin/env python3
"""
Script to add text response support to the database
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

print("Adding text response support...")
print("\nPlease run the following SQL in your Supabase SQL Editor:")
print("=" * 60)

with open('add_text_response_support.sql', 'r') as f:
    sql = f.read()
    print(sql)

print("=" * 60)
print("\nAfter running the SQL, the polls will support:")
print("1. Multiple choice polls (existing functionality)")
print("2. Text response polls (new - students write answers)")
print("\nDone!")
