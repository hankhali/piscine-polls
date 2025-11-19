from flask import Flask, jsonify, request, send_from_directory, Response, session, redirect, url_for
from flask_cors import CORS
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import csv
from io import StringIO
from datetime import datetime
from functools import wraps

# Load environment variables
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Use default static handling and explicitly serve our files from BASE_DIR
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production-' + str(os.urandom(24).hex()))

CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


# Frontend routes
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/admin')
@app.route('/admin/')
def admin_page():
    return send_from_directory(BASE_DIR, 'admin.html')


@app.route('/login.html')
def login_page():
    return send_from_directory(BASE_DIR, 'login.html')


@app.route('/style.css')
def style_css():
    return send_from_directory(BASE_DIR, 'style.css')


@app.route('/app.js')
def app_js():
    return send_from_directory(BASE_DIR, 'app.js')


# Admin authentication routes
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Admin login error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({'success': True})


@app.route('/api/admin/check', methods=['GET'])
def check_admin():
    return jsonify({'logged_in': session.get('admin_logged_in', False)})


# API routes
@app.route('/api/polls', methods=['GET'])
def list_polls():
    # Fetch all polls ordered by ID ascending (oldest first)
    response = supabase.table('polls').select('*, options(*)').order('id', desc=False).execute()
    polls = response.data
    
    data = []
    for p in polls:
        data.append({
            'id': p['id'],
            'title': p['title'],
            'description': p.get('description') or '',
            'poll_type': p.get('poll_type', 'multiple_choice'),  # Add poll_type field
            'opensLabel': p.get('opens_label', 'Opens today'),
            'closesLabel': p.get('closes_label', 'Closes in 3 days'),
            'options': [
                {
                    'id': o['id'],
                    'name': o['name'],
                    'votes': o['votes'],
                }
                for o in (p.get('options') or [])
            ],
        })
    return jsonify({'polls': data})


@app.route('/api/polls', methods=['POST'])
@admin_required
def create_poll():
    try:
        payload = request.get_json(force=True)
        title = (payload.get('title') or '').strip()
        description = (payload.get('description') or '').strip()
        poll_type = (payload.get('poll_type') or 'multiple_choice').strip()
        options = payload.get('options') or []

        options = [str(o).strip() for o in options if str(o).strip()]

        # Validation: text_response polls don't need options, multiple_choice polls do
        if poll_type == 'multiple_choice' and len(options) < 2:
            return jsonify({'error': 'Multiple choice polls require at least two options.'}), 400
        
        if not title:
            return jsonify({'error': 'Title is required.'}), 400

        # Insert poll with poll_type
        poll_response = supabase.table('polls').insert({
            'title': title,
            'description': description,
            'poll_type': poll_type,
            'opens_label': 'Opens today',
            'closes_label': 'Closes in 3 days'
        }).execute()
        
        poll_id = poll_response.data[0]['id']
        
        # Insert options (only for multiple_choice polls)
        if poll_type == 'multiple_choice' and options:
            options_data = [{'name': name, 'poll_id': poll_id, 'votes': 0} for name in options]
            supabase.table('options').insert(options_data).execute()

        return jsonify({'id': poll_id}), 201
    except Exception as e:
        print(f"Error creating poll: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/polls/<int:poll_id>', methods=['DELETE'])
@admin_required
def delete_poll(poll_id):
    # Delete poll (options and votes will be cascade deleted by database)
    supabase.table('polls').delete().eq('id', poll_id).execute()
    return jsonify({'status': 'deleted'})


@app.route('/api/polls/<int:poll_id>', methods=['PUT'])
@admin_required
def update_poll(poll_id):
    """Update poll title, description, type, and options"""
    try:
        payload = request.get_json(force=True)
        print(f"UPDATE POLL {poll_id} - Received payload:", payload)
        title = (payload.get('title') or '').strip()
        description = (payload.get('description') or '').strip()
        poll_type = (payload.get('poll_type') or 'multiple_choice').strip()
        options = payload.get('options', [])
        print(f"  Options received: {options}")
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Validate poll_type
        if poll_type not in ['multiple_choice', 'text_response']:
            return jsonify({'error': 'Invalid poll type'}), 400
        
        # Update the poll
        update_data = {
            'title': title,
            'description': description,
            'poll_type': poll_type
        }
        
        supabase.table('polls').update(update_data).eq('id', poll_id).execute()
        
        # Update options for multiple_choice polls
        if poll_type == 'multiple_choice' and options:
            # Delete existing options
            supabase.table('options').delete().eq('poll_id', poll_id).execute()
            
            # Insert new options
            options_data = [{'name': str(opt).strip(), 'poll_id': poll_id, 'votes': 0} 
                          for opt in options if str(opt).strip()]
            
            if options_data:
                supabase.table('options').insert(options_data).execute()
        
        return jsonify({'status': 'updated', 'id': poll_id})
    except Exception as e:
        print(f"Error updating poll: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/polls/<int:poll_id>/vote', methods=['POST'])
def vote(poll_id):
    payload = request.get_json(force=True)
    option_id = payload.get('option_id')
    username = (payload.get('username') or '').strip()

    if option_id is None:
        return jsonify({'error': 'option_id is required'}), 400

    if not username:
        return jsonify({'error': 'username is required'}), 400

    # Check if option exists
    option_response = supabase.table('options').select('*').eq('id', option_id).eq('poll_id', poll_id).execute()
    if not option_response.data:
        return jsonify({'error': 'Option not found'}), 404

    # Enforce one vote per poll per username
    existing_vote = supabase.table('votes').select('*').eq('poll_id', poll_id).eq('username', username).execute()
    if existing_vote.data:
        return jsonify({'error': 'You have already voted on this poll.'}), 400

    # Increment vote count
    option = option_response.data[0]
    supabase.table('options').update({'votes': option['votes'] + 1}).eq('id', option_id).execute()
    
    # Record the vote
    supabase.table('votes').insert({
        'username': username,
        'poll_id': poll_id,
        'option_id': option_id
    }).execute()

    return jsonify({'status': 'ok'})


@app.route('/api/polls/<int:poll_id>/votes', methods=['GET'])
def poll_votes(poll_id):
    # Check if poll exists
    poll_response = supabase.table('polls').select('*').eq('id', poll_id).execute()
    if not poll_response.data:
        return jsonify({'error': 'Poll not found'}), 404
    
    # Get votes with option details
    votes_response = supabase.table('votes').select('*, options(id, name)').eq('poll_id', poll_id).order('id').execute()
    
    data = [
        {
            'username': v['username'],
            'optionId': v['options']['id'],
            'optionName': v['options']['name'],
        }
        for v in votes_response.data
    ]

    return jsonify({'pollId': poll_id, 'votes': data})


@app.route('/api/polls/<int:poll_id>/votes', methods=['DELETE'])
@admin_required
def clear_poll_votes(poll_id):
    """Clear all votes for a specific poll"""
    try:
        # Check if poll exists
        poll_response = supabase.table('polls').select('*').eq('id', poll_id).execute()
        if not poll_response.data:
            return jsonify({'error': 'Poll not found'}), 404
        
        # Delete all votes for this poll
        supabase.table('votes').delete().eq('poll_id', poll_id).execute()
        
        # Reset vote counts on all options to 0
        options = supabase.table('options').select('id').eq('poll_id', poll_id).execute()
        for option in options.data:
            supabase.table('options').update({'votes': 0}).eq('id', option['id']).execute()
        
        return jsonify({'status': 'ok', 'message': 'All votes cleared successfully'})
    except Exception as e:
        print(f"Error clearing votes: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/polls/<int:poll_id>/text-response', methods=['POST'])
def submit_text_response(poll_id):
    """Submit a text response for a text_response poll"""
    try:
        payload = request.get_json(force=True)
        username = (payload.get('username') or '').strip()
        response_text = (payload.get('response_text') or '').strip()
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        if not response_text:
            return jsonify({'error': 'Response text is required'}), 400
        
        # Check if poll exists and is text_response type
        poll_response = supabase.table('polls').select('*').eq('id', poll_id).execute()
        if not poll_response.data:
            return jsonify({'error': 'Poll not found'}), 404
        
        poll = poll_response.data[0]
        if poll.get('poll_type') != 'text_response':
            return jsonify({'error': 'This poll does not accept text responses'}), 400
        
        # Check if user already responded
        existing = supabase.table('text_responses').select('*').eq('poll_id', poll_id).eq('username', username).execute()
        if existing.data:
            return jsonify({'error': 'You have already responded to this poll'}), 400
        
        # Insert text response
        supabase.table('text_responses').insert({
            'poll_id': poll_id,
            'username': username,
            'response_text': response_text
        }).execute()
        
        return jsonify({'status': 'ok'}), 201
    except Exception as e:
        print(f"Error submitting text response: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/polls/<int:poll_id>/text-responses', methods=['GET'])
def get_text_responses(poll_id):
    """Get all text responses for a poll"""
    try:
        responses = supabase.table('text_responses').select('*').eq('poll_id', poll_id).order('created_at').execute()
        return jsonify({'pollId': poll_id, 'responses': responses.data})
    except Exception as e:
        print(f"Error getting text responses: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/polls/<int:poll_id>/votes/export', methods=['GET'])
@admin_required
def export_poll_votes_csv(poll_id):
    """Export votes for a specific poll as CSV"""
    try:
        # Get poll details
        poll_response = supabase.table('polls').select('*').eq('id', poll_id).execute()
        if not poll_response.data:
            return jsonify({'error': 'Poll not found'}), 404
        
        poll = poll_response.data[0]
        
        # Get votes with option details
        votes_response = supabase.table('votes').select('*, options(name), created_at').eq('poll_id', poll_id).order('created_at').execute()
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Poll ID', 'Poll Title', 'Username', 'Voted For', 'Vote Timestamp'])
        
        # Write votes
        for vote in votes_response.data:
            writer.writerow([
                poll_id,
                poll['title'],
                vote['username'],
                vote['options']['name'],
                vote['created_at']
            ])
        
        # Prepare response
        csv_content = output.getvalue()
        output.close()
        
        # Clean filename - remove emojis and special characters
        import re
        clean_title = re.sub(r'[^\w\s-]', '', poll['title'])
        clean_title = clean_title.replace(' ', '_')[:50]  # Limit length
        filename = f"poll_{poll_id}_{clean_title}_votes.csv"
        
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        print(f"Error exporting poll votes: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/votes/export', methods=['GET'])
@admin_required
def export_all_votes_csv():
    """Export all votes from all polls as CSV"""
    try:
        # Get all votes with poll and option details
        votes_response = supabase.table('votes').select('*, polls(id, title), options(name), created_at').order('created_at').execute()
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Vote ID', 'Poll ID', 'Poll Title', 'Username', 'Voted For', 'Vote Timestamp'])
        
        # Write votes
        for vote in votes_response.data:
            writer.writerow([
                vote['id'],
                vote['polls']['id'],
                vote['polls']['title'],
                vote['username'],
                vote['options']['name'],
                vote['created_at']
            ])
        
        # Prepare response
        csv_content = output.getvalue()
        output.close()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"all_votes_{timestamp}.csv"
        
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        print(f"Error exporting all votes: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/polls/export', methods=['GET'])
@admin_required
def export_polls_summary_csv():
    """Export summary of all polls with vote counts as CSV"""
    try:
        # Get all polls with options
        polls_response = supabase.table('polls').select('*, options(*)').order('id').execute()
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Poll ID', 'Poll Title', 'Description', 'Option Name', 'Votes', 'Created At'])
        
        # Write poll data
        for poll in polls_response.data:
            for option in poll['options']:
                writer.writerow([
                    poll['id'],
                    poll['title'],
                    poll.get('description', ''),
                    option['name'],
                    option['votes'],
                    poll['created_at']
                ])
        
        # Prepare response
        csv_content = output.getvalue()
        output.close()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"polls_summary_{timestamp}.csv"
        
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        print(f"Error exporting polls summary: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run on a non-default port (5001) to avoid macOS services that bind to 5000
    app.run(debug=True, host='127.0.0.1', port=5001)
