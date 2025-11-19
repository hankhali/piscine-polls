# 42 Polling System - Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Database Setup
- [ ] Run the SQL schema in Supabase SQL Editor (`add_text_response_support.sql`)
- [ ] Verify all tables exist: `polls`, `options`, `votes`, `text_responses`
- [ ] Verify RLS policies are enabled
- [ ] Test database connections

### 2. Security Configuration

#### Critical - Change Default Credentials
```bash
# Edit .env file
ADMIN_USERNAME=your_secure_username  # Change from 'admin'
ADMIN_PASSWORD=your_secure_password123!  # Change from 'admin123'
SECRET_KEY=generate_a_random_64_char_string_here
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Recommended Security Enhancements
- [ ] Add rate limiting (Flask-Limiter)
- [ ] Add CSRF protection (Flask-WTF)
- [ ] Enable HTTPS/SSL certificates
- [ ] Set secure session cookies
- [ ] Add input validation and sanitization
- [ ] Implement password hashing (bcrypt) for admin credentials

### 3. Environment Variables
Ensure your `.env` file contains:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SECRET_KEY=your_generated_secret_key_here
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_admin_password
```

### 4. Production Server Setup

#### Install Production Dependencies
```bash
pip install gunicorn
```

Update `requirements.txt`:
```bash
pip freeze > requirements.txt
```

#### Create `Procfile` for deployment (Heroku/Railway/Render)
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

#### Or use gunicorn directly:
```bash
gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --timeout 120
```

### 5. Code Changes for Production

#### Update app.py (bottom of file)
```python
if __name__ == '__main__':
    # Development only
    app.run(debug=True, host='127.0.0.1', port=5001)
```

For production, Gunicorn will handle this. Remove debug=True in production.

#### Add Security Headers
```python
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=True)  # Enable HTTPS enforcement
```

### 6. Static Files
- [ ] Ensure all static files (CSS, JS) are in the correct location
- [ ] Test that style.css and app.js load correctly
- [ ] Verify images/icons if any

### 7. Testing Checklist
- [ ] Test student portal: voting, viewing results
- [ ] Test admin login/logout
- [ ] Test creating polls (both multiple choice and text response)
- [ ] Test editing polls
- [ ] Test deleting polls
- [ ] Test CSV exports
- [ ] Test with multiple users simultaneously
- [ ] Test on mobile devices
- [ ] Test with slow network connection

### 8. Performance Optimization
- [ ] Enable gzip compression
- [ ] Add caching headers for static files
- [ ] Optimize database queries (indexes)
- [ ] Consider CDN for static assets
- [ ] Monitor response times

### 9. Monitoring & Logging
- [ ] Set up error logging (Sentry, LogRocket)
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure alerts for errors
- [ ] Set up analytics (optional)

### 10. Backup Strategy
- [ ] Enable Supabase automated backups
- [ ] Test backup restoration process
- [ ] Document backup procedures

## 🚀 Deployment Platforms

### Option 1: Railway (Recommended - Easy)
1. Connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Railway auto-detects Flask and deploys
4. Custom domain support included

### Option 2: Render
1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Add environment variables

### Option 3: Heroku
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `heroku config:set KEY=value` for each env variable
4. `git push heroku main`

### Option 4: DigitalOcean App Platform
1. Create new app
2. Connect repository
3. Configure environment variables
4. Deploy

### Option 5: VPS (Advanced)
**Requirements:**
- Nginx as reverse proxy
- Supervisor for process management
- SSL certificates (Let's Encrypt)
- Firewall configuration

## 📊 Post-Deployment

### Immediate Actions
- [ ] Change admin password immediately
- [ ] Test all functionality in production
- [ ] Verify SSL certificate
- [ ] Test on multiple devices/browsers
- [ ] Check error logs

### Ongoing Maintenance
- [ ] Weekly: Review error logs
- [ ] Weekly: Check database size and performance
- [ ] Monthly: Update dependencies (security patches)
- [ ] Monthly: Review and rotate admin credentials
- [ ] Quarterly: Database backup verification

## 🔒 Security Best Practices

### Current Implementation
✅ Session-based authentication
✅ Environment variables for sensitive data
✅ RLS (Row Level Security) in Supabase
✅ CORS configuration
✅ Protected admin routes

### Recommended Additions
⚠️ Rate limiting on login endpoint
⚠️ CSRF protection on forms
⚠️ Password complexity requirements
⚠️ Account lockout after failed attempts
⚠️ Two-factor authentication (2FA)
⚠️ Audit logging for admin actions
⚠️ Content Security Policy headers
⚠️ XSS protection headers

## 🐛 Troubleshooting

### Common Issues

**Port 5000 Conflict (macOS)**
- Solution: App now runs on port 5001
- Or use: `export PORT=5001` before running

**Database Connection Errors**
- Verify SUPABASE_URL and SUPABASE_KEY in .env
- Check Supabase project status
- Verify network connectivity

**Static Files Not Loading**
- Check file paths are correct
- Verify Flask is serving from correct directory
- Check browser console for 404 errors

**Admin Login Not Working**
- Verify credentials in .env file
- Check if SECRET_KEY is set
- Clear browser cookies/session

## 📝 Documentation

### API Endpoints
- `GET /` - Student portal
- `GET /admin` - Admin portal (requires login)
- `GET /api/polls` - List all polls
- `POST /api/polls` - Create poll (admin)
- `PUT /api/polls/<id>` - Update poll (admin)
- `DELETE /api/polls/<id>` - Delete poll (admin)
- `POST /api/polls/<id>/vote` - Cast vote
- `GET /api/polls/<id>/votes` - Get vote details (admin)
- `GET /api/polls/<id>/votes/export` - Export CSV (admin)
- `POST /api/admin/login` - Admin login
- `POST /api/admin/logout` - Admin logout

### File Structure
```
polls/
├── app.py              # Main Flask application
├── app.js              # Frontend JavaScript
├── style.css           # Styles (42-theme)
├── index.html          # Student portal
├── admin.html          # Admin portal
├── login.html          # Admin login
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (DO NOT COMMIT)
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
└── Procfile           # Production server config
```

## ✨ Feature Completion Status

### Implemented
✅ Multiple choice voting polls
✅ Admin authentication system
✅ Edit poll questions from admin panel
✅ CSV export functionality
✅ Bar chart visualizations
✅ Vote tracking and analytics
✅ Responsive 42-style UI
✅ Session management
✅ Database migrations

### Ready to Implement
⏳ Text response polls (schema ready, needs API + UI)
⏳ Rate limiting
⏳ CSRF protection

## 💡 Notes

- **Port**: Production apps typically use PORT from environment variable
- **Workers**: 2-4 Gunicorn workers recommended for small apps
- **Timeout**: 120 seconds handles slow database queries
- **Database**: Supabase handles connection pooling automatically
- **Scaling**: Consider moving to dedicated database if > 10k users

## 🆘 Support

For issues:
1. Check error logs first
2. Verify environment variables
3. Test database connectivity
4. Check Supabase dashboard for issues
5. Review this checklist again

---

**Last Updated**: November 2025
**Version**: 1.0
