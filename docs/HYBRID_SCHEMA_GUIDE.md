# 🔄 Hybrid Schema Guide

## What is a Hybrid Schema?

A **hybrid schema** combines the best of both worlds:
1. **Structured fields** - Fixed columns for common data (fast queries, validation)
2. **Flexible JSONB** - Store ANY custom data without schema changes

This means you can store **any type of document** while maintaining performance and searchability.

---

## 🎯 Why Hybrid?

### Traditional Approach (Rigid)
```sql
-- Can ONLY store Q&A
question TEXT
answer TEXT
```
❌ Can't add new fields without altering table  
❌ All entries must follow same structure  
❌ Limited to one document type  

### Pure JSONB Approach (Too Flexible)
```sql
-- Everything in JSON
data JSONB
```
❌ Slow queries (no indexes on common fields)  
❌ No validation  
❌ Hard to search efficiently  

### Hybrid Approach (Best of Both) ✅
```sql
-- Common fields (structured)
question TEXT
answer TEXT
category TEXT

-- Custom fields (flexible)
content JSONB
metadata JSONB
```
✅ Fast queries on common fields  
✅ Store ANY custom data  
✅ Maintain data integrity  
✅ No schema changes needed  

---

## 📊 Schema Overview

### Core Fields (Always Available)
```sql
id              -- Unique identifier
question        -- The question (REQUIRED)
answer          -- The answer (REQUIRED)
```

### Media Fields (Rich Content)
```sql
media_url       -- Primary media (image, video, PDF)
media_type      -- Type: 'image', 'video', 'pdf', 'document', 'code'
media_urls      -- JSONB: Multiple media of different types
```

### Document Type (Flexible)
```sql
content_type    -- 'qa', 'document', 'tutorial', 'policy', 
                -- 'faq', 'code', 'troubleshooting', 'reference'
```

### Rich Content (ANYTHING!)
```sql
content         -- JSONB: Store ANY structured data
                -- - Full documents
                -- - Code snippets
                -- - Step-by-step guides
                -- - Tables, lists
                -- - Nested structures
```

### Source Tracking
```sql
source_type     -- 'confluence', 'figma', 'manual', 'api', 
                -- 'jira', 'notion', 'github'
source_id       -- External ID (page ID, file key, etc.)
source_url      -- Direct link to source
source_parent_id -- For hierarchical content
last_synced     -- When last updated
```

### Organization
```sql
category        -- Main category
subcategory     -- Sub-category (nested)
tags            -- Array of tags
priority        -- Importance (0-10)
```

### Access Control
```sql
is_public       -- Public or private
required_role   -- Who can access
department      -- Which department owns it
```

### Lifecycle
```sql
status          -- 'active', 'draft', 'archived', 'deprecated'
expiry_date     -- When info becomes outdated
created_at      -- When created
updated_at      -- When last modified
```

### Metadata (ANYTHING ELSE!)
```sql
metadata        -- JSONB: Store ANY additional data
```

---

## 💡 Use Cases & Examples

### 1. Simple Q&A (Chatbot)
```sql
INSERT INTO knowledge_base (question, answer, content_type)
VALUES (
    'What is AI?',
    'Artificial Intelligence is...',
    'qa'
);
```

### 2. Q&A with Image
```sql
INSERT INTO knowledge_base (
    question, answer, media_url, media_type
) VALUES (
    'Show me the architecture',
    'Here is the system architecture',
    'https://example.com/diagram.png',
    'image'
);
```

### 3. Full Document (Confluence)
```sql
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    source_type,
    source_id
) VALUES (
    'What is our vacation policy?',
    'See full policy details',
    'policy',
    '{
        "sections": [
            {"heading": "Eligibility", "content": "..."},
            {"heading": "Accrual", "content": "..."}
        ],
        "effective_date": "2026-01-01"
    }'::jsonb,
    'confluence',
    'page-12345'
);
```

### 4. Code Snippet (GitHub)
```sql
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    source_type
) VALUES (
    'How to connect to database?',
    'Use this code snippet',
    'code',
    '{
        "language": "python",
        "code": "from supabase import create_client...",
        "dependencies": ["supabase"]
    }'::jsonb,
    'github'
);
```

### 5. Tutorial with Steps
```sql
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content
) VALUES (
    'How to deploy to production?',
    'Follow these steps',
    'tutorial',
    '{
        "steps": [
            {"number": 1, "title": "Build", "command": "npm run build"},
            {"number": 2, "title": "Test", "command": "npm test"},
            {"number": 3, "title": "Deploy", "command": "vercel deploy"}
        ],
        "duration": "15 minutes"
    }'::jsonb
);
```

### 6. Troubleshooting Guide
```sql
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    priority
) VALUES (
    'How to fix timeout error?',
    'Follow troubleshooting steps',
    'troubleshooting',
    '{
        "problem": "Connection Timeout",
        "symptoms": ["Request takes >30s", "Error message"],
        "steps": [
            {"step": 1, "action": "Check network"},
            {"step": 2, "action": "Verify firewall"}
        ]
    }'::jsonb,
    8  -- High priority
);
```

### 7. Multiple Media (Images + Videos + PDFs)
```sql
INSERT INTO knowledge_base (
    question,
    answer,
    media_urls
) VALUES (
    'How to set up dev environment?',
    'See video tutorial and docs',
    '{
        "images": ["screenshot1.png", "screenshot2.png"],
        "videos": ["https://youtube.com/..."],
        "pdfs": ["setup-guide.pdf"]
    }'::jsonb
);
```

### 8. Hierarchical Content (Parent-Child)
```sql
-- Parent
INSERT INTO knowledge_base (
    question, answer, source_id
) VALUES (
    'Employee Handbook',
    'Complete employee handbook',
    'parent-001'
);

-- Child
INSERT INTO knowledge_base (
    question, answer, source_id, source_parent_id
) VALUES (
    'Chapter 1: Getting Started',
    'First day information',
    'child-001',
    'parent-001'  -- Links to parent
);
```

### 9. API Reference
```sql
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content
) VALUES (
    'What are the API endpoints?',
    'Complete API reference',
    'reference',
    '{
        "api_version": "v2",
        "endpoints": [
            {
                "method": "GET",
                "path": "/users",
                "parameters": {"limit": "integer"},
                "example": "curl https://api.com/users"
            }
        ]
    }'::jsonb
);
```

### 10. Custom Metadata (Anything!)
```sql
INSERT INTO knowledge_base (
    question,
    answer,
    metadata
) VALUES (
    'Product launch plan',
    'Q2 2026 launch details',
    '{
        "launch_date": "2026-04-15",
        "team": ["Alice", "Bob", "Carol"],
        "budget": 50000,
        "milestones": [
            {"date": "2026-03-01", "task": "Beta release"},
            {"date": "2026-04-01", "task": "Marketing campaign"}
        ],
        "custom_field_1": "any value",
        "custom_field_2": {"nested": "data"}
    }'::jsonb
);
```

---

## 🔍 Querying Hybrid Data

### Basic Queries
```sql
-- All Q&As
SELECT * FROM knowledge_base WHERE content_type = 'qa';

-- All tutorials
SELECT * FROM knowledge_base WHERE content_type = 'tutorial';

-- All from Confluence
SELECT * FROM knowledge_base WHERE source_type = 'confluence';

-- High priority items
SELECT * FROM knowledge_base WHERE priority >= 8 ORDER BY priority DESC;
```

### JSONB Queries
```sql
-- Find Python code examples
SELECT * FROM knowledge_base 
WHERE content_type = 'code' 
AND content->>'language' = 'python';

-- Find tutorials longer than 20 minutes
SELECT * FROM knowledge_base 
WHERE content_type = 'tutorial'
AND (content->>'duration')::text LIKE '%20%';

-- Find policies effective after 2026
SELECT * FROM knowledge_base 
WHERE content_type = 'policy'
AND content->>'effective_date' > '2026-01-01';

-- Find content with specific metadata
SELECT * FROM knowledge_base 
WHERE metadata->>'team' IS NOT NULL;
```

### Hierarchical Queries
```sql
-- Find all children of a parent
SELECT * FROM knowledge_base 
WHERE source_parent_id = 'parent-001';

-- Find parent of a child
SELECT p.* FROM knowledge_base c
JOIN knowledge_base p ON c.source_parent_id = p.source_id
WHERE c.id = 123;
```

### Full-Text Search
```sql
-- Search across question and answer
SELECT * FROM knowledge_base 
WHERE to_tsvector('english', question || ' ' || answer) 
@@ plainto_tsquery('english', 'machine learning');
```

---

## ✅ Benefits of Hybrid Schema

### 1. **Flexibility**
- Store ANY document type
- Add custom fields without schema changes
- Support multiple content formats

### 2. **Performance**
- Fast queries on indexed fields
- Efficient full-text search
- Optimized for common operations

### 3. **Maintainability**
- No schema migrations for new fields
- Easy to extend
- Backward compatible

### 4. **Scalability**
- Handles millions of entries
- Efficient storage
- Supports complex queries

### 5. **Future-Proof**
- Add new document types anytime
- Store evolving data structures
- No breaking changes

---

## 🎯 Best Practices

### 1. Use Structured Fields for Common Data
```sql
-- ✅ Good: Use dedicated columns
category TEXT
tags TEXT[]

-- ❌ Avoid: Putting common data in JSONB
metadata->>'category'  -- Slower queries
```

### 2. Use JSONB for Variable/Custom Data
```sql
-- ✅ Good: Custom fields in JSONB
content JSONB  -- Different structure per document type
metadata JSONB -- Truly custom data

-- ❌ Avoid: Creating columns for rare fields
special_field_only_used_once TEXT  -- Wastes space
```

### 3. Index Important JSONB Fields
```sql
-- Create index on frequently queried JSONB field
CREATE INDEX idx_content_language 
ON knowledge_base ((content->>'language'));
```

### 4. Validate JSONB Structure in Application
```python
# Validate before inserting
def validate_tutorial(content):
    required = ['steps', 'duration']
    return all(k in content for k in required)
```

### 5. Document Your JSONB Structures
```python
# Document expected structure
TUTORIAL_SCHEMA = {
    "steps": [{"number": int, "title": str, "command": str}],
    "duration": str,
    "difficulty": str  # optional
}
```

---

## 🚀 Migration Path

### From Hardcoded Array
```python
# Old: Hardcoded
KNOWLEDGE_BASE = [
    {"question": "...", "answer": "..."}
]

# New: Hybrid database
supabase.table('knowledge_base').insert({
    "question": "...",
    "answer": "...",
    "content_type": "qa"
}).execute()
```

### From Confluence
```python
# Extract page
page = confluence.get_page(page_id)

# Store in hybrid schema
supabase.table('knowledge_base').insert({
    "question": page['title'],
    "answer": page['body'],
    "content_type": "document",
    "content": {
        "sections": parse_sections(page['body']),
        "attachments": page['attachments']
    },
    "source_type": "confluence",
    "source_id": page_id
}).execute()
```

### From Figma
```python
# Extract design
design = figma.get_design_context(file_key, node_id)

# Store in hybrid schema
supabase.table('knowledge_base').insert({
    "question": f"How to use {design['component_name']}?",
    "answer": design['description'],
    "content_type": "reference",
    "content": {
        "component_props": design['properties'],
        "variants": design['variants']
    },
    "media_url": design['screenshot_url'],
    "source_type": "figma",
    "source_id": node_id
}).execute()
```

---

## 📚 Summary

The **hybrid schema** gives you:

✅ **Structure** where you need it (fast queries)  
✅ **Flexibility** where you want it (any data)  
✅ **Performance** (indexed common fields)  
✅ **Scalability** (handles any document type)  
✅ **Future-proof** (no schema changes needed)  

You can store:
- Simple Q&As
- Full documents
- Code snippets
- Tutorials
- Policies
- API docs
- Troubleshooting guides
- **Literally anything!**

All in one table, with fast queries and full flexibility! 🎉
