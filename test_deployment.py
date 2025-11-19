#!/usr/bin/env python3
"""
Automated Pre-Deployment Tests
Tests critical functionality before deployment
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name, passed, message=""):
    status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
    print(f"{status} - {name}")
    if message:
        print(f"  {YELLOW}→{RESET} {message}")

def print_section(title):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

# Load environment variables
load_dotenv()

# Test counters
tests_passed = 0
tests_failed = 0
warnings = 0

print(f"{BLUE}🧪 Running Pre-Deployment Tests...{RESET}\n")

# ============================================================================
# Test 1: Environment Variables
# ============================================================================
print_section("1. Environment Variables")

required_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'SECRET_KEY', 'ADMIN_USERNAME', 'ADMIN_PASSWORD']
env_tests_passed = 0

for var in required_vars:
    value = os.getenv(var)
    if value and len(value.strip()) > 0:
        print_test(f"{var} exists", True)
        env_tests_passed += 1
        tests_passed += 1
    else:
        print_test(f"{var} exists", False, "Missing or empty")
        tests_failed += 1

# ============================================================================
# Test 2: Supabase Connection
# ============================================================================
print_section("2. Supabase Connection")

try:
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print_test("Supabase credentials", False, "Missing URL or KEY")
        tests_failed += 1
    else:
        supabase = create_client(supabase_url, supabase_key)
        print_test("Create Supabase client", True)
        tests_passed += 1
        
        # Test database connection
        try:
            response = supabase.table('polls').select('id').limit(1).execute()
            print_test("Database connection", True, f"Connected successfully")
            tests_passed += 1
        except Exception as e:
            error_msg = str(e)
            if 'SSL' in error_msg or 'Connection reset' in error_msg:
                print_test("Database connection", False, "SSL/Network error - check Supabase status")
                warnings += 1
            else:
                print_test("Database connection", False, error_msg[:100])
            tests_failed += 1
            
except Exception as e:
    print_test("Supabase setup", False, str(e)[:100])
    tests_failed += 1

# ============================================================================
# Test 3: Database Schema
# ============================================================================
print_section("3. Database Schema")

try:
    # Check if poll_type column exists
    response = supabase.table('polls').select('poll_type').limit(1).execute()
    print_test("polls.poll_type column exists", True)
    tests_passed += 1
except Exception as e:
    error_msg = str(e)
    if 'poll_type' in error_msg or 'PGRST204' in error_msg:
        print_test("polls.poll_type column exists", False, 
                  "❗ CRITICAL: Run add_text_response_support.sql in Supabase!")
        print(f"  {RED}→ Go to Supabase Dashboard → SQL Editor{RESET}")
        print(f"  {RED}→ Run the SQL from add_text_response_support.sql{RESET}")
    else:
        print_test("polls.poll_type column exists", False, error_msg[:100])
    tests_failed += 1

try:
    # Check if text_responses table exists
    response = supabase.table('text_responses').select('id').limit(1).execute()
    print_test("text_responses table exists", True)
    tests_passed += 1
except Exception as e:
    error_msg = str(e)
    if 'does not exist' in error_msg or 'relation' in error_msg:
        print_test("text_responses table exists", False,
                  "Run add_text_response_support.sql")
    else:
        print_test("text_responses table exists", False, error_msg[:100])
    tests_failed += 1

try:
    # Check if options table exists
    response = supabase.table('options').select('id').limit(1).execute()
    print_test("options table exists", True)
    tests_passed += 1
except Exception as e:
    print_test("options table exists", False, "Missing required table")
    tests_failed += 1

try:
    # Check if votes table exists
    response = supabase.table('votes').select('id').limit(1).execute()
    print_test("votes table exists", True)
    tests_passed += 1
except Exception as e:
    print_test("votes table exists", False, "Missing required table")
    tests_failed += 1

# ============================================================================
# Test 4: Data Integrity
# ============================================================================
print_section("4. Data Integrity")

try:
    # Check if polls exist
    response = supabase.table('polls').select('id').execute()
    poll_count = len(response.data)
    print_test(f"Polls exist", poll_count > 0, f"Found {poll_count} polls")
    if poll_count > 0:
        tests_passed += 1
    else:
        warnings += 1
        print(f"  {YELLOW}⚠ No polls found - create some test polls{RESET}")
    
    # Check poll order
    response = supabase.table('polls').select('id').order('id', desc=False).execute()
    ids = [p['id'] for p in response.data]
    is_ascending = all(ids[i] <= ids[i+1] for i in range(len(ids)-1)) if len(ids) > 1 else True
    print_test("Polls ordered by ID ascending", is_ascending)
    if is_ascending:
        tests_passed += 1
    else:
        tests_failed += 1
        
except Exception as e:
    print_test("Data checks", False, str(e)[:100])
    tests_failed += 1

# ============================================================================
# Test 5: Required Files
# ============================================================================
print_section("5. Required Files")

required_files = [
    'app.py',
    'app.js',
    'style.css',
    'index.html',
    'admin.html',
    'login.html',
    'requirements.txt',
    'Procfile',
    '.env'
]

for file in required_files:
    exists = os.path.exists(file)
    print_test(f"{file} exists", exists)
    if exists:
        tests_passed += 1
    else:
        tests_failed += 1

# ============================================================================
# Test 6: Port Availability
# ============================================================================
print_section("6. Server Configuration")

import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

port_5001_in_use = is_port_in_use(5001)
if port_5001_in_use:
    print_test("Port 5001 available", False, "Port already in use - server might be running")
    warnings += 1
else:
    print_test("Port 5001 available", True)
    tests_passed += 1

# ============================================================================
# Final Report
# ============================================================================
print_section("Test Results Summary")

total_tests = tests_passed + tests_failed
pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0

print(f"\nTotal Tests: {total_tests}")
print(f"{GREEN}Passed: {tests_passed}{RESET}")
print(f"{RED}Failed: {tests_failed}{RESET}")
print(f"{YELLOW}Warnings: {warnings}{RESET}")
print(f"\nPass Rate: {pass_rate:.1f}%\n")

if tests_failed > 0:
    print(f"{RED}{'='*60}{RESET}")
    print(f"{RED}❌ TESTS FAILED - DO NOT DEPLOY YET{RESET}")
    print(f"{RED}{'='*60}{RESET}")
    print(f"\n{YELLOW}Critical Actions Required:{RESET}")
    print("1. Run add_text_response_support.sql in Supabase SQL Editor")
    print("2. Fix any SSL/connection errors")
    print("3. Ensure all environment variables are set")
    print("4. Re-run this test script")
    sys.exit(1)
elif warnings > 0:
    print(f"{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}⚠️  TESTS PASSED WITH WARNINGS{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")
    print(f"\n{YELLOW}Review warnings before deploying{RESET}")
    sys.exit(0)
else:
    print(f"{GREEN}{'='*60}{RESET}")
    print(f"{GREEN}✅ ALL TESTS PASSED - READY TO DEPLOY!{RESET}")
    print(f"{GREEN}{'='*60}{RESET}")
    print(f"\n{GREEN}Next steps:{RESET}")
    print("1. Test manually in browser (http://localhost:5001)")
    print("2. Review PRE_DEPLOYMENT_CHECKLIST.md")
    print("3. Deploy to your hosting platform")
    print("4. Test again on production URL")
    sys.exit(0)
