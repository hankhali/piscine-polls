# Polls Application - Supabase Setup Guide

This application has been migrated from SQLite to Supabase (PostgreSQL).

## Setup Instructions

### 1. Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in
3. Create a new project
4. Wait for the project to be ready

### 2. Create Database Tables

1. Go to your Supabase project dashboard
2. Click on "SQL Editor" in the left sidebar
3. Click "New query"
4. Copy the contents of `supabase_schema.sql` and paste it into the editor
5. Click "Run" to execute the SQL

This will create:
- `polls` table - stores poll information
- `options` table - stores poll options
- `votes` table - stores user votes with unique constraint per poll

### 3. Get Your Supabase Credentials

1. In your Supabase project, go to "Settings" (gear icon in the left sidebar)
2. Click on "API" in the settings menu
3. You'll find:
   - **Project URL** - this is your `SUPABASE_URL`
   - **Project API keys** - use the `anon` / `public` key as your `SUPABASE_KEY`

### 4. Configure Environment Variables

1. Open the `.env` file in this project
2. Replace the placeholder values with your actual Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Important**: Never commit the `.env` file to version control!

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

- `app.py` - Flask application with Supabase integration
- `requirements.txt` - Python dependencies
- `supabase_schema.sql` - Database schema for Supabase
- `.env` - Environment variables (not committed to git)
- `index.html` - Student voting interface
- `admin.html` - Admin poll management interface
- `app.js` - Frontend JavaScript
- `style.css` - Styling

## API Endpoints

- `GET /api/polls` - List all polls
- `POST /api/polls` - Create a new poll
- `DELETE /api/polls/<poll_id>` - Delete a poll
- `POST /api/polls/<poll_id>/vote` - Submit a vote
- `GET /api/polls/<poll_id>/votes` - Get all votes for a poll

## Security Notes

The current setup uses Row Level Security (RLS) policies that allow public access. For production use, you should:

1. Implement proper authentication
2. Restrict RLS policies based on authenticated users
3. Add rate limiting
4. Validate input more thoroughly
5. Consider using Supabase Auth for user management

## Troubleshooting

### "SUPABASE_URL and SUPABASE_KEY must be set"
- Make sure your `.env` file exists and has the correct values
- Check that the variable names match exactly

### Connection errors
- Verify your Supabase URL and key are correct
- Check that your Supabase project is running
- Ensure your internet connection is working

### Table doesn't exist errors
- Make sure you ran the `supabase_schema.sql` in your Supabase SQL Editor
- Check the "Table Editor" in Supabase to verify the tables were created

## Migration Notes

This application was migrated from:
- **Old**: Flask-SQLAlchemy with SQLite
- **New**: Supabase Python Client with PostgreSQL

Key changes:
- Removed `Flask-SQLAlchemy` dependency
- Added `supabase` and `python-dotenv` dependencies
- Replaced all database queries with Supabase client calls
- Tables now in Supabase cloud database instead of local SQLite file
