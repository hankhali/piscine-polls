-- Useful SQL Queries for Your Polls Database
-- Copy these into Supabase SQL Editor

-- 1. View all polls with their option count and total votes
SELECT 
    p.id,
    p.title,
    p.description,
    p.created_at,
    COUNT(DISTINCT o.id) as option_count,
    COALESCE(SUM(o.votes), 0) as total_votes
FROM polls p
LEFT JOIN options o ON p.id = o.poll_id
GROUP BY p.id, p.title, p.description, p.created_at
ORDER BY p.created_at DESC;

-- 2. View a specific poll with all its options and vote counts
SELECT 
    p.id as poll_id,
    p.title as poll_title,
    o.id as option_id,
    o.name as option_name,
    o.votes
FROM polls p
JOIN options o ON p.id = o.poll_id
WHERE p.id = 1  -- Change this to your poll ID
ORDER BY o.votes DESC;

-- 3. View all votes with username and what they voted for
SELECT 
    v.id,
    v.username,
    p.title as poll_title,
    o.name as voted_for,
    v.created_at
FROM votes v
JOIN polls p ON v.poll_id = p.id
JOIN options o ON v.option_id = o.id
ORDER BY v.created_at DESC;

-- 4. See who voted on a specific poll
SELECT 
    v.username,
    o.name as voted_for,
    v.created_at
FROM votes v
JOIN options o ON v.option_id = o.id
WHERE v.poll_id = 1  -- Change this to your poll ID
ORDER BY v.created_at DESC;

-- 5. Get voting statistics per poll
SELECT 
    p.id,
    p.title,
    COUNT(DISTINCT v.username) as unique_voters,
    COUNT(v.id) as total_votes,
    COUNT(DISTINCT o.id) as options_count
FROM polls p
LEFT JOIN votes v ON p.id = v.poll_id
LEFT JOIN options o ON p.id = o.poll_id
GROUP BY p.id, p.title
ORDER BY unique_voters DESC;

-- 6. Find most popular option across all polls
SELECT 
    p.title as poll_title,
    o.name as option_name,
    o.votes,
    RANK() OVER (PARTITION BY p.id ORDER BY o.votes DESC) as rank_in_poll
FROM options o
JOIN polls p ON o.poll_id = p.id
ORDER BY p.id, o.votes DESC;

-- 7. See users who voted multiple times (across different polls)
SELECT 
    username,
    COUNT(*) as polls_voted_in,
    STRING_AGG(DISTINCT p.title, ', ') as polls
FROM votes v
JOIN polls p ON v.poll_id = p.id
GROUP BY username
HAVING COUNT(*) > 1
ORDER BY polls_voted_in DESC;
