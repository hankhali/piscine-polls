#!/usr/bin/env python3
"""
View polls, options, and votes from Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def view_all_polls():
    """Display all polls with their options"""
    print("\n" + "="*80)
    print("📊 ALL POLLS")
    print("="*80)
    
    response = supabase.table('polls').select('*, options(*)').order('id').execute()
    
    if not response.data:
        print("No polls found.")
        return
    
    for poll in response.data:
        print(f"\n🗳️  Poll #{poll['id']}: {poll['title']}")
        print(f"   Description: {poll['description'] or 'N/A'}")
        print(f"   Created: {poll['created_at']}")
        print(f"\n   Options:")
        total_votes = 0
        for opt in poll['options']:
            print(f"      • {opt['name']}: {opt['votes']} votes")
            total_votes += opt['votes']
        print(f"\n   Total Votes: {total_votes}")
        print("-" * 80)

def view_all_votes():
    """Display all votes with details"""
    print("\n" + "="*80)
    print("✅ ALL VOTES")
    print("="*80)
    
    response = supabase.table('votes').select('*, polls(title), options(name)').order('created_at').execute()
    
    if not response.data:
        print("No votes found.")
        return
    
    for vote in response.data:
        print(f"👤 {vote['username']} voted for '{vote['options']['name']}'")
        print(f"   Poll: {vote['polls']['title']}")
        print(f"   Time: {vote['created_at']}")
        print("-" * 40)

def view_poll_details(poll_id):
    """View detailed information about a specific poll"""
    print(f"\n" + "="*80)
    print(f"📋 POLL DETAILS - ID #{poll_id}")
    print("="*80)
    
    # Get poll with options
    poll_response = supabase.table('polls').select('*, options(*)').eq('id', poll_id).execute()
    
    if not poll_response.data:
        print(f"Poll #{poll_id} not found.")
        return
    
    poll = poll_response.data[0]
    
    print(f"\nTitle: {poll['title']}")
    print(f"Description: {poll['description'] or 'N/A'}")
    print(f"Created: {poll['created_at']}")
    
    # Get votes
    votes_response = supabase.table('votes').select('*, options(name)').eq('poll_id', poll_id).execute()
    
    print(f"\n📊 VOTING RESULTS:")
    print("-" * 80)
    
    total_votes = 0
    for opt in poll['options']:
        votes = opt['votes']
        total_votes += votes
        percentage = (votes / total_votes * 100) if total_votes > 0 else 0
        bar = "█" * int(percentage / 2)
        print(f"{opt['name']:<30} {votes:>3} votes  {percentage:>5.1f}% {bar}")
    
    print(f"\nTotal Votes: {total_votes}")
    print(f"Unique Voters: {len(votes_response.data)}")
    
    if votes_response.data:
        print(f"\n👥 WHO VOTED:")
        print("-" * 40)
        for vote in votes_response.data:
            print(f"   {vote['username']} → {vote['options']['name']}")

def view_statistics():
    """Display overall statistics"""
    print("\n" + "="*80)
    print("📈 DATABASE STATISTICS")
    print("="*80)
    
    polls = supabase.table('polls').select('*').execute()
    options = supabase.table('options').select('*').execute()
    votes = supabase.table('votes').select('*').execute()
    
    total_votes = sum(opt['votes'] for opt in options.data)
    unique_voters = len(set(vote['username'] for vote in votes.data))
    
    print(f"\n📊 Total Polls: {len(polls.data)}")
    print(f"📝 Total Options: {len(options.data)}")
    print(f"✅ Total Votes Cast: {total_votes}")
    print(f"👥 Unique Voters: {unique_voters}")
    
    if polls.data:
        avg_options = len(options.data) / len(polls.data)
        avg_votes = total_votes / len(polls.data) if len(polls.data) > 0 else 0
        print(f"📊 Average Options per Poll: {avg_options:.1f}")
        print(f"✅ Average Votes per Poll: {avg_votes:.1f}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'votes':
            view_all_votes()
        elif command == 'stats':
            view_statistics()
        elif command.startswith('poll='):
            poll_id = int(command.split('=')[1])
            view_poll_details(poll_id)
        else:
            print("Unknown command. Use: votes, stats, or poll=<id>")
    else:
        # Default: show everything
        view_statistics()
        view_all_polls()
        view_all_votes()
