# Pre-Deployment Checklist ✅

## Critical: Database Migration Required

### Step 1: Apply Database Schema
**YOU MUST DO THIS FIRST!**

1. Go to your Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to **SQL Editor** (left sidebar)
4. Click **New Query**
5. Copy and paste the entire content of `add_text_response_support.sql`
6. Click **Run** or press Cmd+Enter
7. Verify success message

**What this adds:**
- `poll_type` column to polls table (multiple_choice or text_response)
- `text_responses` table for text-based polls
- RLS policies for public access

---

## Testing Checklist

### 1. Database Connection ✓
- [ ] `.env` file exists with valid credentials
- [ ] SUPABASE_URL is correct
- [ ] SUPABASE_KEY is valid (anon/public key)
- [ ] No SSL errors when connecting

### 2. Admin Portal Tests
- [ ] Can login with credentials from `.env`
- [ ] Can view all polls
- [ ] Can create new multiple choice poll with options
- [ ] Can edit existing poll
  - [ ] Can change title/description
  - [ ] Can switch between Multiple Choice and Text Response
  - [ ] Can add/remove options for Multiple Choice
- [ ] Can delete poll
- [ ] Can view vote details (click View button)
- [ ] Can export votes to CSV (individual poll)
- [ ] Can export all votes to CSV
- [ ] Bar charts display correctly
- [ ] Text response polls show "📝 Text Response Poll" instead of chart

### 3. Student Portal Tests
- [ ] Polls display in correct order (ascending by ID)
- [ ] Cards are uniform width and height
- [ ] View buttons aligned at same position
- [ ] "Closes in 3 days" text is readable (not too big/bold)
- [ ] Stats show correct labels (CAND/VOTES/TIME or TYPE/RESP/TIME)

#### Multiple Choice Polls:
- [ ] Can select a candidate
- [ ] Vote button becomes active when candidate selected
- [ ] Can submit vote successfully
- [ ] After voting, shows "VOTED" button (disabled)
- [ ] After voting, shows bar chart with results
- [ ] Winner highlighted in results

#### Text Response Polls:
- [ ] Shows textarea input for response
- [ ] Placeholder text visible
- [ ] Can type and submit response
- [ ] After submitting, shows "✅ Thank you for your response!"
- [ ] Cannot submit empty response
- [ ] Cannot submit twice (stored in localStorage)

### 4. UI/UX Tests
- [ ] All cards same width/height
- [ ] View buttons perfectly aligned
- [ ] Footer "STATUS: ACTIVE" and vote button properly spaced
- [ ] Stat values not too large
- [ ] Poll descriptions truncate with ellipsis if too long
- [ ] Hover effects work on buttons
- [ ] Modal dialogs styled correctly
- [ ] Select dropdowns match theme (cyan arrows)
- [ ] Options list in edit dialog works (add/remove)

### 5. Authentication Tests
- [ ] Admin portal redirects to login if not authenticated
- [ ] Login works with correct credentials
- [ ] Login fails with wrong credentials
- [ ] Logout works
- [ ] Session persists on page refresh
- [ ] Student portal accessible without login

### 6. Data Integrity Tests
- [ ] Poll order remains consistent (ascending by ID)
- [ ] Vote counts accurate
- [ ] No duplicate votes per user
- [ ] CSV exports contain all data
- [ ] Text responses saved correctly
- [ ] Options updates don't lose votes (check before updating live polls!)

### 7. Error Handling Tests
- [ ] Shows error if trying to vote twice
- [ ] Shows error if selecting no candidate
- [ ] Shows error if submitting empty text response
- [ ] Shows error on network failures
- [ ] Graceful handling of missing poll data

### 8. Browser Compatibility
- [ ] Test in Chrome
- [ ] Test in Safari
- [ ] Test in Firefox
- [ ] Hard refresh works (Cmd+Shift+R)
- [ ] No console errors

---

## Known Issues to Fix Before Deployment

### Issue 1: Missing poll_type Column
**Status:** ❌ NOT FIXED
**Fix:** Run `add_text_response_support.sql` in Supabase SQL Editor
**Impact:** Cannot edit polls or use text response feature

### Issue 2: SSL Connection Errors
**Status:** ⚠️ INTERMITTENT
**Possible causes:**
- Network issue
- Supabase rate limiting
- Invalid credentials
- Expired Supabase project

**Fix:** 
1. Check Supabase dashboard - is project paused?
2. Verify credentials in `.env`
3. Try regenerating Supabase anon key
4. Check Supabase status: https://status.supabase.com/

---

## Environment Variables Checklist
Make sure `.env` contains:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
SECRET_KEY=your-random-secret-key
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-admin-password
```

---

## Deployment Steps

### For Railway/Render/Heroku:
1. ✅ Run database migration first
2. ✅ Test everything locally
3. Set environment variables in platform
4. Deploy from GitHub or direct upload
5. Test deployed site immediately
6. Monitor logs for errors

### Post-Deployment Tests:
- [ ] Can access student portal at production URL
- [ ] Can access admin portal at production URL
- [ ] Can login to admin
- [ ] Can create and vote on polls
- [ ] CSS loads correctly (no caching issues)
- [ ] API endpoints respond correctly

---

## Rollback Plan
If something breaks:
1. Keep local version running
2. Check error logs on hosting platform
3. Verify environment variables set correctly
4. Check Supabase connection from production
5. Rollback to previous Git commit if needed

---

## Support
If issues persist:
1. Check Flask terminal for Python errors
2. Check browser console for JavaScript errors
3. Check Supabase logs in dashboard
4. Verify all files uploaded correctly
5. Test API endpoints directly (curl/Postman)
