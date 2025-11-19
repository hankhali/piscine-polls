# 🧪 Manual Testing Checklist for Polls App

## ✅ Backend Tests: PASSED
- ✅ Multiple-choice poll creation works
- ✅ Voting on multiple-choice polls works
- ✅ Text-response poll creation works
- ✅ Submitting text responses works
- ✅ Reading responses works

---

## 🌐 Browser Testing Steps

### Part 1: Test Multiple-Choice Poll (Create & Vote)

#### Admin Side - Create Poll
1. **Open Admin Panel:** http://localhost:5001/admin
   - Username: `admin` (or check your .env file)
   - Password: `admin123` (or check your .env file)

2. **Create a Multiple-Choice Poll:**
   - Click on the "Create New Poll" section
   - Title: `🧪 TEST: Favorite Snack`
   - Description: `What's your favorite coding snack?`
   - **Poll Type:** Select `Multiple Choice`
   - Options: 
     - Add option: `Coffee`
     - Add option: `Pizza`
     - Add option: `Energy Drink`
   - Click "CREATE POLL"
   - ✅ Poll should appear in the list

#### Student Side - Vote on Poll
3. **Switch to Student View:**
   - Click the "< Student View" link at the top
   - Enter a username (e.g., `testuser1`)
   - Click "START VOTING"

4. **Vote on Your Poll:**
   - Find the "TEST: Favorite Snack" poll
   - Click on one of the options (e.g., `Coffee`)
   - The option should highlight
   - Click "SUBMIT VOTE"
   - ✅ Should see "Vote submitted!" message
   - ✅ Try voting again - should see error (duplicate vote prevention)

#### Verify Results
5. **Check Admin Panel:**
   - Click "> Admin Panel" to go back
   - Find your test poll
   - Click "VIEW" to see results
   - ✅ Should see 1 vote for the option you selected
   - ✅ Bar chart should display correctly

---

### Part 2: Test Text-Response Poll (Create & Submit)

#### Admin Side - Create Text Poll
6. **Create a Text-Response Poll:**
   - Scroll to "Create New Poll" section
   - Title: `🧪 TEST: Best Memory`
   - Description: `Share your best Piscine memory!`
   - **Poll Type:** Select `Text Response`
   - Click "CREATE POLL"
   - ✅ Poll should appear (no options shown - it's text-based)

#### Student Side - Submit Response
7. **Switch to Student View:**
   - Click "< Student View"
   - Find the "TEST: Best Memory" poll

8. **Submit a Text Response:**
   - Type something in the text area (e.g., `Making new friends during rush`)
   - Click "SUBMIT RESPONSE"
   - ✅ Should see "Response submitted!" message
   - ✅ Try submitting again - should see error (duplicate prevention)

#### Verify Text Responses
9. **Check Admin Panel:**
   - Go back to Admin Panel
   - Find your text poll
   - Click "VIEW" to see responses
   - ✅ Should see your text response
   - ✅ Should show username and timestamp

---

### Part 3: Test Export & Delete

#### Test CSV Export
10. **Export Poll Data:**
    - On any poll, click the "📊 CSV" button
    - ✅ Should download a CSV file
    - ✅ Open it - should contain vote/response data

#### Test Edit Functionality
11. **Edit a Poll:**
    - Click "✏️ EDIT" on any poll
    - Change the title or description
    - Click "UPDATE POLL"
    - ✅ Changes should be saved and visible

#### Test Delete Functionality
12. **Delete Test Polls:**
    - On your test polls, click the 🗑️ (trash) icon
    - Confirm deletion
    - ✅ Polls should disappear from the list

---

## 🐛 Things to Check For:

### Security & Validation
- [ ] Can't vote without entering username
- [ ] Can't vote twice on same poll with same username
- [ ] Can't submit empty text response
- [ ] Admin panel requires login
- [ ] Wrong admin password shows error

### UI/UX
- [ ] Polls display in correct order (1, 2, 3, 4, 5...)
- [ ] Vote counts update correctly
- [ ] Text responses display properly
- [ ] Buttons are responsive and work
- [ ] Error messages are clear

### Data Integrity
- [ ] Votes persist after page refresh
- [ ] Text responses persist after page refresh
- [ ] Poll order stays correct
- [ ] CSV exports contain correct data

---

## 🎯 Expected Results

After completing all tests, you should have:
- ✅ Created 2 test polls (multiple-choice + text-response)
- ✅ Voted on the multiple-choice poll
- ✅ Submitted a text response
- ✅ Viewed results in admin panel
- ✅ Exported data to CSV
- ✅ Deleted test polls

---

## 🚨 If Something Doesn't Work:

1. **Check the browser console** (F12 → Console tab)
2. **Check terminal logs** (where Flask is running)
3. **Verify you're logged in** (for admin functions)
4. **Try refreshing the page**
5. **Check your .env file** has correct credentials

---

## 📝 Notes:

- Test polls created by script (IDs 15 & 16) can be deleted via admin panel
- Always test with a fresh username to avoid "already voted" errors
- The application is now production-ready after these tests pass!

---

**Good luck with testing! 🚀**
