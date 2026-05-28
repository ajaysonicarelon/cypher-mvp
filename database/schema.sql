-- ============================================================================
-- AI Chatbot Knowledge Base Schema - HYBRID DESIGN
-- ============================================================================
-- 🔄 HYBRID SCHEMA: Combines structured fields + flexible JSONB
-- 
-- This schema supports:
-- ✅ Simple Q&A (chatbot style)
-- ✅ Full documents (Confluence pages, policies, guides)
-- ✅ Code snippets (GitHub, examples)
-- ✅ Tutorials (step-by-step guides)
-- ✅ Troubleshooting guides
-- ✅ API reference documentation
-- ✅ ANY custom document type
-- 
-- Key Features:
-- - Structured fields for common data (fast queries)
-- - JSONB fields for flexible content (any structure)
-- - Multiple media support (images, videos, PDFs)
-- - Source tracking (Confluence, Figma, Jira, GitHub, etc.)
-- - Hierarchical content (parent-child relationships)
-- - Smart sync with UPSERT capability
-- - Access control & lifecycle management
-- - Full-text search & advanced indexing
-- 
-- See: docs/HYBRID_SCHEMA_GUIDE.md for complete documentation
-- See: database/hybrid_examples.sql for usage examples
-- ============================================================================

-- Drop existing table if you want to start fresh (CAUTION: deletes all data)
-- DROP TABLE IF EXISTS knowledge_base CASCADE;

-- Main knowledge base table (HYBRID SCHEMA)
CREATE TABLE IF NOT EXISTS knowledge_base (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- Core Q&A content (REQUIRED - for chatbot)
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    
    -- Media & Rich Content (FLEXIBLE - any type)
    media_url TEXT,              -- Primary media (image, video, PDF)
    media_type TEXT,             -- 'image', 'video', 'pdf', 'document', 'code', 'link'
    media_urls JSONB,            -- Multiple media: {"images": [...], "videos": [...], "pdfs": [...]}
    
    -- Document Type (HYBRID - supports any format)
    content_type TEXT DEFAULT 'qa' CHECK (content_type IN (
        'qa',              -- Question & Answer (default)
        'document',        -- Full document/article
        'tutorial',        -- Step-by-step guide
        'policy',          -- Company policy/procedure
        'faq',             -- FAQ entry
        'code',            -- Code snippet/example
        'troubleshooting', -- Troubleshooting guide
        'reference',       -- Reference documentation
        'other'            -- Any other type
    )),
    
    -- Rich Content Storage (FLEXIBLE - any structure)
    content JSONB,               -- Store ANY structured data:
                                 -- - Full documents
                                 -- - Code snippets with syntax
                                 -- - Step-by-step instructions
                                 -- - Tables, lists, etc.
    
    -- Source tracking (for sync)
    source_type TEXT CHECK (source_type IN ('confluence', 'figma', 'manual', 'api', 'jira', 'notion', 'github')),
    source_id TEXT,              -- Page ID, File key, Issue ID, etc.
    source_url TEXT,             -- Direct link to source document
    source_parent_id TEXT,       -- Parent page/section ID (for hierarchy)
    last_synced TIMESTAMP,       -- When this entry was last synced
    
    -- Organization & filtering
    category TEXT,
    subcategory TEXT,            -- For nested categorization
    tags TEXT[],                 -- Array of tags for filtering
    priority INTEGER DEFAULT 0,  -- For ranking/ordering (higher = more important)
    
    -- Access Control (OPTIONAL - for future use)
    is_public BOOLEAN DEFAULT true,
    required_role TEXT,          -- 'admin', 'employee', 'manager', etc.
    department TEXT,             -- 'IT', 'HR', 'Engineering', etc.
    
    -- Status & Lifecycle
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'draft', 'archived', 'deprecated')),
    expiry_date TIMESTAMP,       -- When this info becomes outdated
    
    -- Flexible metadata storage (ANYTHING ELSE)
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Prevent duplicate questions from same source
    CONSTRAINT unique_question_source UNIQUE(question, source_type)
);

-- ============================================================================
-- Indexes for performance
-- ============================================================================

-- Full-text search index on question and answer
CREATE INDEX IF NOT EXISTS idx_knowledge_base_search 
ON knowledge_base USING gin(to_tsvector('english', question || ' ' || answer));

-- Index for source lookups (for sync operations)
CREATE INDEX IF NOT EXISTS idx_knowledge_base_source 
ON knowledge_base(source_type, source_id);

-- Index for category filtering
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category 
ON knowledge_base(category);

-- Index for tag searches
CREATE INDEX IF NOT EXISTS idx_knowledge_base_tags 
ON knowledge_base USING gin(tags);

-- Index for metadata queries
CREATE INDEX IF NOT EXISTS idx_knowledge_base_metadata 
ON knowledge_base USING gin(metadata);

-- Index for last_synced (to find stale entries)
CREATE INDEX IF NOT EXISTS idx_knowledge_base_last_synced 
ON knowledge_base(last_synced);

-- Index for content type filtering
CREATE INDEX IF NOT EXISTS idx_knowledge_base_content_type 
ON knowledge_base(content_type);

-- Index for status filtering
CREATE INDEX IF NOT EXISTS idx_knowledge_base_status 
ON knowledge_base(status);

-- Index for department/access control
CREATE INDEX IF NOT EXISTS idx_knowledge_base_department 
ON knowledge_base(department);

-- Index for priority ordering
CREATE INDEX IF NOT EXISTS idx_knowledge_base_priority 
ON knowledge_base(priority DESC);

-- Index for rich content queries
CREATE INDEX IF NOT EXISTS idx_knowledge_base_content 
ON knowledge_base USING gin(content);

-- Index for multiple media
CREATE INDEX IF NOT EXISTS idx_knowledge_base_media_urls 
ON knowledge_base USING gin(media_urls);

-- Index for hierarchical queries
CREATE INDEX IF NOT EXISTS idx_knowledge_base_parent 
ON knowledge_base(source_parent_id);

-- ============================================================================
-- Trigger to auto-update updated_at timestamp
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_knowledge_base_updated_at
    BEFORE UPDATE ON knowledge_base
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Optional: Version history table (uncomment if you want to track changes)
-- ============================================================================

/*
CREATE TABLE IF NOT EXISTS knowledge_base_history (
    history_id SERIAL PRIMARY KEY,
    kb_id INTEGER REFERENCES knowledge_base(id) ON DELETE CASCADE,
    question TEXT,
    answer TEXT,
    media_url TEXT,
    changed_at TIMESTAMP DEFAULT NOW(),
    changed_by TEXT,
    change_type TEXT CHECK (change_type IN ('insert', 'update', 'delete'))
);

-- Trigger to log changes to history
CREATE OR REPLACE FUNCTION log_knowledge_base_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        INSERT INTO knowledge_base_history (kb_id, question, answer, media_url, change_type)
        VALUES (OLD.id, OLD.question, OLD.answer, OLD.media_url, 'update');
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO knowledge_base_history (kb_id, question, answer, media_url, change_type)
        VALUES (OLD.id, OLD.question, OLD.answer, OLD.media_url, 'delete');
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER knowledge_base_history_trigger
    AFTER UPDATE OR DELETE ON knowledge_base
    FOR EACH ROW
    EXECUTE FUNCTION log_knowledge_base_changes();
*/

-- ============================================================================
-- Useful views
-- ============================================================================

-- View for recently synced entries
CREATE OR REPLACE VIEW recent_syncs AS
SELECT 
    id,
    question,
    source_type,
    source_url,
    last_synced,
    EXTRACT(EPOCH FROM (NOW() - last_synced))/3600 as hours_since_sync
FROM knowledge_base
WHERE last_synced IS NOT NULL
ORDER BY last_synced DESC;

-- View for entries by source
CREATE OR REPLACE VIEW entries_by_source AS
SELECT 
    source_type,
    COUNT(*) as entry_count,
    MAX(last_synced) as last_sync_time
FROM knowledge_base
GROUP BY source_type;

-- ============================================================================
-- Helper functions
-- ============================================================================

-- Function to search knowledge base (for testing)
CREATE OR REPLACE FUNCTION search_knowledge_base(search_query TEXT)
RETURNS TABLE (
    id INTEGER,
    question TEXT,
    answer TEXT,
    relevance REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        kb.id,
        kb.question,
        kb.answer,
        ts_rank(
            to_tsvector('english', kb.question || ' ' || kb.answer),
            plainto_tsquery('english', search_query)
        ) as relevance
    FROM knowledge_base kb
    WHERE to_tsvector('english', kb.question || ' ' || kb.answer) @@ plainto_tsquery('english', search_query)
    ORDER BY relevance DESC;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- Row Level Security (RLS) - Optional, uncomment if needed
-- ============================================================================

/*
-- Enable RLS
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can read
CREATE POLICY "Allow public read access"
ON knowledge_base FOR SELECT
USING (true);

-- Policy: Only authenticated users can insert/update
CREATE POLICY "Allow authenticated insert"
ON knowledge_base FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated update"
ON knowledge_base FOR UPDATE
USING (auth.role() = 'authenticated');
*/

-- ============================================================================
-- Grant permissions (adjust based on your Supabase setup)
-- ============================================================================

-- Grant access to anon and authenticated roles
GRANT SELECT ON knowledge_base TO anon, authenticated;
GRANT INSERT, UPDATE, DELETE ON knowledge_base TO authenticated;
GRANT USAGE ON SEQUENCE knowledge_base_id_seq TO authenticated;

-- ============================================================================
-- Success message
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ HYBRID Knowledge Base Schema Created Successfully!';
    RAISE NOTICE '';
    RAISE NOTICE '� HYBRID DESIGN:';
    RAISE NOTICE '   ✓ Structured fields for fast queries';
    RAISE NOTICE '   ✓ JSONB fields for flexible content';
    RAISE NOTICE '   ✓ Supports ANY document type';
    RAISE NOTICE '';
    RAISE NOTICE '�📊 Database Objects:';
    RAISE NOTICE '   • Table: knowledge_base (hybrid schema)';
    RAISE NOTICE '   • Indexes: 14 created for optimal performance';
    RAISE NOTICE '   • Triggers: auto-update timestamp enabled';
    RAISE NOTICE '   • Views: recent_syncs, entries_by_source';
    RAISE NOTICE '   • Functions: search_knowledge_base()';
    RAISE NOTICE '';
    RAISE NOTICE '� Supports:';
    RAISE NOTICE '   ✓ Q&A (chatbot)';
    RAISE NOTICE '   ✓ Full documents (Confluence, Notion)';
    RAISE NOTICE '   ✓ Code snippets (GitHub)';
    RAISE NOTICE '   ✓ Tutorials & guides';
    RAISE NOTICE '   ✓ Policies & procedures';
    RAISE NOTICE '   ✓ API documentation';
    RAISE NOTICE '   ✓ ANY custom content!';
    RAISE NOTICE '';
    RAISE NOTICE '�📝 Next steps:';
    RAISE NOTICE '   1. Run seed_data.sql to populate initial data';
    RAISE NOTICE '   2. See hybrid_examples.sql for usage examples';
    RAISE NOTICE '   3. Read docs/HYBRID_SCHEMA_GUIDE.md for details';
    RAISE NOTICE '   4. Test connection with: python database/test_connection.py';
    RAISE NOTICE '   5. Start syncing from MCP sources (Confluence, Figma)';
END $$;
