-- Disable Row Level Security for testing
-- Run this in Supabase SQL Editor if you get RLS errors

ALTER TABLE knowledge_base DISABLE ROW LEVEL SECURITY;

-- Verify RLS is disabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'knowledge_base';

-- Expected output: rowsecurity = false
