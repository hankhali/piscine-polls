-- Supabase Schema for Polls Application
-- Run this SQL in your Supabase SQL Editor to create the tables

-- Create polls table
CREATE TABLE IF NOT EXISTS polls (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    opens_label VARCHAR(255) DEFAULT 'Opens today',
    closes_label VARCHAR(255) DEFAULT 'Closes in 3 days',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create options table
CREATE TABLE IF NOT EXISTS options (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    votes INTEGER DEFAULT 0,
    poll_id BIGINT NOT NULL REFERENCES polls(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create votes table
CREATE TABLE IF NOT EXISTS votes (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    poll_id BIGINT NOT NULL REFERENCES polls(id) ON DELETE CASCADE,
    option_id BIGINT NOT NULL REFERENCES options(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(poll_id, username) -- Ensure one vote per user per poll
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_options_poll_id ON options(poll_id);
CREATE INDEX IF NOT EXISTS idx_votes_poll_id ON votes(poll_id);
CREATE INDEX IF NOT EXISTS idx_votes_option_id ON votes(option_id);
CREATE INDEX IF NOT EXISTS idx_votes_username ON votes(username);

-- Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE polls ENABLE ROW LEVEL SECURITY;
ALTER TABLE options ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust based on your security needs)
-- Allow anyone to read polls and options
CREATE POLICY "Allow public read access to polls" ON polls
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access to options" ON options
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access to votes" ON votes
    FOR SELECT USING (true);

-- Allow anyone to insert polls, options, and votes (you may want to restrict this)
CREATE POLICY "Allow public insert to polls" ON polls
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public insert to options" ON options
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public insert to votes" ON votes
    FOR INSERT WITH CHECK (true);

-- Allow anyone to update options (for vote counts)
CREATE POLICY "Allow public update to options" ON options
    FOR UPDATE USING (true);

-- Allow anyone to delete polls (you may want to restrict this)
CREATE POLICY "Allow public delete to polls" ON polls
    FOR DELETE USING (true);
