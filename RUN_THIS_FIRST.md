# 🚨 CRITICAL: Database Migration Required

## You MUST do this before the app will work!

### Step-by-Step Instructions:

1. **Open Supabase Dashboard**
   - Go to: https://supabase.com/dashboard
   - Login to your account
   - Select your project: `zdqslvnyqbudglbndyva`

2. **Open SQL Editor**
   - Click on "SQL Editor" in the left sidebar
   - Or go directly to: https://supabase.com/dashboard/project/zdqslvnyqbudglbndyva/sql

3. **Create New Query**
   - Click the "New Query" button (or "+" button)

4. **Copy and Paste the SQL**
   - Open the file: `add_text_response_support.sql`
   - Select ALL the content (Cmd+A)
   - Copy it (Cmd+C)
   - Paste into the Supabase SQL Editor (Cmd+V)

5. **Run the Migration**
   - Click the "Run" button
   - OR press `Cmd + Enter`

6. **Verify Success**
   - You should see: "Success. No rows returned"
   - This is normal and correct!

7. **Test the Fix**
   - Come back to your terminal
   - Run: `python test_deployment.py`
   - All tests should now pass!

---

## What This Migration Does:

✅ Adds `poll_type` column to polls table  
✅ Creates `text_responses` table for text-based polls  
✅ Sets up RLS (Row Level Security) policies  
✅ Enables text response feature

---

## If You See Errors:

**"relation does not exist"**  
→ Wrong table name, check your schema

**"column already exists"**  
→ Good! The migration was already run

**"permission denied"**  
→ Make sure you're using the service_role key in .env

---

## After Running Migration:

1. Run the test script: `python test_deployment.py`
2. Restart your Flask server: `make`
3. Test in browser: http://localhost:5001/admin
4. Try editing a poll - you should now see "Poll Type" dropdown!

---

## Need Help?

Check:
- Supabase Dashboard → Project Settings → API
- Make sure your SUPABASE_KEY in .env is the `service_role` key (not anon)
- The service_role key has admin access to run migrations
