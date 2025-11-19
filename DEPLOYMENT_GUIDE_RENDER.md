# 🚀 Deployment Guide - Piscine Polls to Render

## Prerequisites
- ✅ GitHub account
- ✅ Render account (free): https://render.com
- ✅ Your code ready in a GitHub repository

## Step 1: Push Your Code to GitHub

If you haven't already, push your code to GitHub:

```bash
cd /Users/hanieh/Desktop/polls

# Initialize git if not done
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/piscine-polls.git

# Push to GitHub
git push -u origin main
```

## Step 2: Sign Up / Login to Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email
4. Verify your email if needed

## Step 3: Create New Web Service

1. From Render Dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click "Connect" next to GitHub
   - Authorize Render to access your repositories
   - Select your `piscine-polls` repository

## Step 4: Configure Your Web Service

Fill in these settings:

### Basic Settings:
- **Name:** `piscine-polls` (or any name you want)
- **Region:** Choose closest to your users (e.g., Oregon, Frankfurt)
- **Branch:** `main` (or your default branch)
- **Root Directory:** Leave blank
- **Runtime:** Python 3

### Build & Deploy Settings:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120`

### Instance Type:
- **Plan:** Select **"Free"** (this is sufficient for your app)

## Step 5: Add Environment Variables ⚠️ CRITICAL

Click **"Advanced"** and add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `SUPABASE_URL` | `https://zdqslvnyqbudglbndyva.supabase.co` | Your Supabase project URL |
| `SUPABASE_KEY` | `YOUR_SUPABASE_KEY` | Your service_role key from .env |
| `ADMIN_USERNAME` | `admin` | Admin login username |
| `ADMIN_PASSWORD` | `admin123` | Admin login password |
| `PYTHON_VERSION` | `3.11.0` | Python version |

**How to get your Supabase Key:**
1. Check your `.env` file
2. Copy the value of `SUPABASE_KEY`
3. Paste it in Render

## Step 6: Deploy!

1. Click **"Create Web Service"** button at the bottom
2. Render will start building your app (takes 2-5 minutes)
3. Watch the logs in real-time
4. Wait for "Your service is live 🎉" message

## Step 7: Get Your Live URL

Once deployed, you'll see:
- **Live URL:** `https://piscine-polls.onrender.com` (or similar)
- This is your public URL - share it with students!

## Step 8: Test Your Deployed App

1. **Student View:** Visit `https://your-app.onrender.com/`
   - Should show all 5 polls
   - Students can vote

2. **Admin View:** Visit `https://your-app.onrender.com/admin.html`
   - Login with: admin / admin123
   - Create, edit, manage polls

## 🎯 Important Notes

### Free Tier Limitations:
- ⏰ App "sleeps" after 15 minutes of inactivity
- 🐌 First request after sleep takes ~30-60 seconds to wake up
- 📊 750 hours/month free (enough for small projects)

### Keep App Awake (Optional):
If you want faster response times, use a ping service:
- https://uptimerobot.com (free)
- Ping your URL every 14 minutes

### Custom Domain (Optional):
1. Go to your service settings in Render
2. Click "Custom Domain"
3. Add your domain and follow DNS instructions

## 🔧 Troubleshooting

### Build Fails:
- Check logs in Render dashboard
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

### App Crashes:
- Check environment variables are set correctly
- Verify SUPABASE_URL and SUPABASE_KEY
- Check application logs in Render

### Can't Login to Admin:
- Verify `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables
- Try redeploying after fixing

### Database Connection Issues:
- Verify Supabase URL is correct
- Check Supabase key has correct permissions (use service_role key)
- Ensure Supabase project is active

## 📱 Sharing Your App

Once deployed, share these URLs:

**For Students:**
```
https://your-app.onrender.com/
```

**For Admins:**
```
https://your-app.onrender.com/admin.html
Username: admin
Password: admin123
```

## 🔄 Updating Your App

To push updates:

```bash
# Make your changes
git add .
git commit -m "Update description"
git push

# Render will automatically redeploy!
```

## 🎉 You're Live!

Your polls application is now accessible worldwide! Students can vote from any device with a browser.

---

**Need help?** Check Render's documentation: https://render.com/docs
