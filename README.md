# 42 Polling System

A Flask-based polling application with Supabase integration, featuring separate admin and student portals with vote tracking, CSV exports, and visual analytics.

## Features

### Student Portal (/)
- View active polls
- Cast votes (one vote per poll per username)
- View results with bar chart visualizations
- No authentication required

### Admin Portal (/admin)
- **Secure login required** (username: `admin`, password: `admin123`)
- Create new polls with multiple options
- View detailed vote tracking (who voted for what)
- Export data to CSV:
  - Individual poll votes
  - All votes across all polls
  - Poll summary with vote counts
- Visual bar charts showing results
- Delete polls (cascades to options and votes)
- Logout functionality

## Setup

1. **Install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Create a `.env` file with:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   SECRET_KEY=your_secret_key_for_sessions
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin123
   ```

3. **Set up Supabase database:**
   - Create a new project at [supabase.com](https://supabase.com)
   - Run the SQL schema from `supabase_schema.sql`

4. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at http://localhost:5000

## Routes

- `/` - Student portal (no login required)
- `/admin` - Admin portal (requires authentication)
- `/login.html` - Admin login page
- `/api/polls` - GET: List all polls, POST: Create poll (admin only)
- `/api/polls/<id>` - DELETE: Delete poll (admin only)
- `/api/polls/<id>/vote` - POST: Cast a vote
- `/api/polls/<id>/votes` - GET: Get votes for a poll
- `/api/polls/<id>/votes/export` - GET: Export poll votes as CSV (admin only)
- `/api/votes/export` - GET: Export all votes as CSV (admin only)
- `/api/polls/export` - GET: Export poll summary as CSV (admin only)
- `/api/admin/login` - POST: Admin login
- `/api/admin/logout` - POST: Admin logout
- `/api/admin/check` - GET: Check admin authentication status

## Database Schema

### Tables
- **polls**: Poll information (id, title, description, labels)
- **options**: Poll options (id, poll_id, name, votes)
- **votes**: Vote records (id, poll_id, option_id, username, timestamp)

### Relationships
- `options.poll_id` → `polls.id` (CASCADE DELETE)
- `votes.poll_id` → `polls.id` (CASCADE DELETE)
- `votes.option_id` → `options.id` (CASCADE DELETE)

### Constraints
- Unique constraint on `votes(poll_id, username)` - one vote per user per poll

## Security

- Admin routes protected with session-based authentication
- CORS enabled for API access
- Environment variables for sensitive data
- Row Level Security (RLS) policies in Supabase
- Password stored in environment variables (change in production!)

## Development

- Flask debug mode enabled
- Auto-reload on code changes
- Detailed error logging
- CSS with 42-style theme (cyan/orange color scheme)

## Production Considerations

1. **Change default credentials**: Update `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`
2. **Use strong SECRET_KEY**: Generate a secure random key
3. **Use production WSGI server**: Replace Flask dev server with Gunicorn or uWSGI
4. **Enable HTTPS**: Use SSL/TLS certificates
5. **Secure Supabase**: Review RLS policies and API keys
6. **Add rate limiting**: Protect against brute force attacks
7. **Add CSRF protection**: Use Flask-WTF or similar

## Technologies

- **Backend**: Flask 3.0.0
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Vanilla JavaScript with CSS3 animations
- **Authentication**: Flask session-based auth
- **Data Export**: Python CSV module

## License

MIT
