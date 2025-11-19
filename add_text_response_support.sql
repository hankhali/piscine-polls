-- Add poll_type column to polls table
-- 'multiple_choice' = traditional voting with options
-- 'text_response' = students write text answers

ALTER TABLE polls 
ADD COLUMN IF NOT EXISTS poll_type VARCHAR(50) DEFAULT 'multiple_choice';

-- Create text_responses table for text-based answers
CREATE TABLE IF NOT EXISTS text_responses (
    id BIGSERIAL PRIMARY KEY,
    poll_id BIGINT NOT NULL REFERENCES polls(id) ON DELETE CASCADE,
    username VARCHAR(255) NOT NULL,
    response_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(poll_id, username)
);

-- Add RLS policies for text_responses
ALTER TABLE text_responses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read access to text_responses" ON text_responses;
CREATE POLICY "Allow public read access to text_responses" 
ON text_responses FOR SELECT 
TO public 
USING (true);

DROP POLICY IF EXISTS "Allow public insert access to text_responses" ON text_responses;
CREATE POLICY "Allow public insert access to text_responses" 
ON text_responses FOR INSERT 
TO public 
WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public update access to text_responses" ON text_responses;
CREATE POLICY "Allow public update access to text_responses" 
ON text_responses FOR UPDATE 
TO public 
USING (true);

DROP POLICY IF EXISTS "Allow public delete access to text_responses" ON text_responses;
CREATE POLICY "Allow public delete access to text_responses" 
ON text_responses FOR DELETE 
TO public 
USING (true);

-- Add comment
COMMENT ON TABLE text_responses IS 'Stores text responses for text-based polls';
COMMENT ON COLUMN polls.poll_type IS 'Type of poll: multiple_choice or text_response';
