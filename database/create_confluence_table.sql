-- Create table for storing Confluence pages
CREATE TABLE IF NOT EXISTS confluence_pages (
    id BIGSERIAL PRIMARY KEY,
    page_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    content TEXT NOT NULL,
    keywords TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on page_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_confluence_page_id ON confluence_pages(page_id);

-- Create index on keywords for faster searches
CREATE INDEX IF NOT EXISTS idx_confluence_keywords ON confluence_pages USING GIN(keywords);

-- Create full-text search index on content
CREATE INDEX IF NOT EXISTS idx_confluence_content_search ON confluence_pages USING GIN(to_tsvector('english', content));

COMMENT ON TABLE confluence_pages IS 'Stores extracted Confluence page content with keywords for better searchability';
COMMENT ON COLUMN confluence_pages.page_id IS 'Confluence page ID extracted from URL';
COMMENT ON COLUMN confluence_pages.keywords IS 'Extracted keywords from content for better search';
