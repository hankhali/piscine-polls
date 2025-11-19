# 🚀 DEPLOY YOUR POLLS APP IN 10 MINUTES

## ✅ Step 1: Create GitHub Repository (5 minutes)

1. Go to https://github.com/new
2. Repository name: `piscine-polls`
3. Description: `Piscine Polls - Voting application for 42 students`
4. Keep it **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **"Create repository"**

## ✅ Step 2: Push Your Code (1 minute)

Copy and run these commands in your terminal:

```bash
cd /Users/hanieh/Desktop/polls

# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/piscine-polls.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:** If your GitHub username is `hanieh42`, use:
```bash
git remote add origin https://github.com/hanieh42/piscine-polls.git
```

## ✅ Step 3: Sign Up for Render (2 minutes)

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest option)
4. Authorize Render to access your repositories

## ✅ Step 4: Deploy Your App (2 minutes)

1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Find your `piscine-polls` repository and click **"Connect"**

### Configure the service:
- **Name:** `piscine-polls`
- **Region:** Choose closest to you
- **Branch:** `main`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120`
- **Plan:** Free

### ⚠️ IMPORTANT - Add Environment Variables:

Click **"Add Environment Variable"** and add these 3:

| Variable | Value |
|----------|-------|
| `SUPABASE_URL` | Copy from your `.env` file |
| `SUPABASE_KEY` | Copy from your `.env` file |
| `ADMIN_PASSWORD` | `admin123` |

**To get your values:**
```bash
cat /Users/hanieh/Desktop/polls/.env
```

4. Click **"Create Web Service"**

## ✅ Step 5: Wait for Deployment (3-5 minutes)

Watch the build logs. You'll see:
- Installing dependencies...
- Building...
- Deploying...
- ✅ **"Your service is live 🎉"**

## 🎉 YOU'RE LIVE!

Your app URL will be something like:
```
https://piscine-polls.onrender.com
```

### Share these links:

**Students vote here:**
```
https://piscine-polls.onrender.com/
```

**Admin panel:**
```
https://piscine-polls.onrender.com/admin.html
Login: admin / admin123
```

---

## 🔧 Troubleshooting

### "Application failed to respond"
- Check environment variables are set correctly
- View logs in Render dashboard
- Ensure SUPABASE_KEY is the service_role key

### "Can't login to admin"
- Check ADMIN_PASSWORD environment variable
- Default is: admin123

### Need to update your app?
```bash
cd /Users/hanieh/Desktop/polls
git add .
git commit -m "Updated features"
git push
# Render auto-deploys!
```

---

## 📱 Free Tier Notes

- App sleeps after 15 min of inactivity
- First request takes 30-60 seconds to wake up
- 750 hours/month free (plenty for your project)

---

**That's it! Your polls are now live and accessible worldwide! 🌍**
