# 🔄 Hybrid Schema Quick Reference

## What Can You Store?

| Document Type | Example | Uses |
|--------------|---------|------|
| **Q&A** | "What is AI?" → "AI is..." | Chatbot responses |
| **Document** | Full Confluence page | Policies, guides, handbooks |
| **Tutorial** | Step-by-step guide | How-to instructions |
| **Code** | Python snippet | Code examples, templates |
| **Troubleshooting** | Fix error X | Problem-solution guides |
| **Reference** | API documentation | Technical specs |
| **FAQ** | Multiple Q&As | Common questions |
| **Policy** | HR policy document | Company policies |
| **Custom** | Anything else! | Your imagination |

---

## Core Structure

### Required Fields (Always)
```sql
question    TEXT      -- The question/title
answer      TEXT      -- The answer/summary
```

### Optional Structured Fields
```sql
media_url       TEXT      -- Primary image/video/PDF
media_type      TEXT      -- Type of media
media_urls      JSONB     -- Multiple media files
content_type    TEXT      -- Document type (qa, tutorial, etc.)
category        TEXT      -- Main category
subcategory     TEXT      -- Sub-category
tags            TEXT[]    -- Array of tags
priority        INTEGER   -- Importance (0-10)
department      TEXT      -- Owning department
status          TEXT      -- active, draft, archived
```

### Flexible JSONB Fields (Anything!)
```sql
content         JSONB     -- ANY structured content
metadata        JSONB     -- ANY custom data
```

### Source Tracking
```sql
source_type     TEXT      -- confluence, figma, github, etc.
source_id       TEXT      -- External ID
source_url      TEXT      -- Direct link
source_parent_id TEXT     -- For hierarchical content
last_synced     TIMESTAMP -- When last updated
```

---

## Quick Examples

### 1. Simple Q&A
```sql
INSERT INTO knowledge_base (question, answer)
VALUES ('What is AI?', 'Artificial Intelligence is...');
```

### 2. With Image
```sql
INSERT INTO knowledge_base (question, answer, media_url, media_type)
VALUES (
    'Show architecture',
    'Here is the diagram',
    'https://example.com/diagram.png',
    'image'
);
```

### 3. Tutorial
```sql
INSERT INTO knowledge_base (
    question, answer, content_type, content
) VALUES (
    'How to deploy?',
    'Follow these steps',
    'tutorial',
    '{"steps": [{"number": 1, "action": "Build"}, {"number": 2, "action": "Deploy"}]}'::jsonb
);
```

### 4. Code Snippet
```sql
INSERT INTO knowledge_base (
    question, answer, content_type, content
) VALUES (
    'How to connect DB?',
    'Use this code',
    'code',
    '{"language": "python", "code": "import supabase..."}'::jsonb
);
```

### 5. From Confluence
```sql
INSERT INTO knowledge_base (
    question, answer, source_type, source_id, source_url, last_synced
) VALUES (
    'Vacation Policy',
    'See full policy',
    'confluence',
    'page-123',
    'https://company.atlassian.net/wiki/...',
    NOW()
);
```

### 6. Custom Metadata
```sql
INSERT INTO knowledge_base (
    question, answer, metadata
) VALUES (
    'Product Launch',
    'Q2 2026 launch',
    '{"launch_date": "2026-04-15", "budget": 50000, "custom_field": "any value"}'::jsonb
);
```

---

## Common Queries

### By Type
```sql
-- All tutorials
SELECT * FROM knowledge_base WHERE content_type = 'tutorial';

-- All code examples
SELECT * FROM knowledge_base WHERE content_type = 'code';
```

### By Source
```sql
-- From Confluence
SELECT * FROM knowledge_base WHERE source_type = 'confluence';

-- From Figma
SELECT * FROM knowledge_base WHERE source_type = 'figma';
```

### By Priority
```sql
-- High priority items
SELECT * FROM knowledge_base WHERE priority >= 8 ORDER BY priority DESC;
```

### By Category
```sql
-- HR content
SELECT * FROM knowledge_base WHERE category = 'hr';

-- With subcategory
SELECT * FROM knowledge_base WHERE category = 'hr' AND subcategory = 'benefits';
```

### By Tags
```sql
-- Has 'python' tag
SELECT * FROM knowledge_base WHERE 'python' = ANY(tags);
```

### JSONB Queries
```sql
-- Python code
SELECT * FROM knowledge_base 
WHERE content_type = 'code' 
AND content->>'language' = 'python';

-- Tutorials > 20 min
SELECT * FROM knowledge_base 
WHERE content_type = 'tutorial'
AND (content->>'duration') LIKE '%20%';
```

### Hierarchical
```sql
-- Find children
SELECT * FROM knowledge_base WHERE source_parent_id = 'parent-id';

-- Find parent
SELECT p.* FROM knowledge_base c
JOIN knowledge_base p ON c.source_parent_id = p.source_id
WHERE c.id = 123;
```

---

## Python Examples

### Insert Simple Q&A
```python
supabase.table('knowledge_base').insert({
    "question": "What is AI?",
    "answer": "Artificial Intelligence is...",
    "content_type": "qa",
    "category": "ai-basics",
    "tags": ["ai", "basics"]
}).execute()
```

### Insert Tutorial
```python
supabase.table('knowledge_base').insert({
    "question": "How to deploy?",
    "answer": "Follow these steps",
    "content_type": "tutorial",
    "content": {
        "steps": [
            {"number": 1, "action": "Build", "command": "npm run build"},
            {"number": 2, "action": "Deploy", "command": "vercel deploy"}
        ],
        "duration": "10 minutes"
    },
    "tags": ["deployment", "tutorial"]
}).execute()
```

### Insert from Confluence
```python
supabase.table('knowledge_base').insert({
    "question": page['title'],
    "answer": page['excerpt'],
    "content_type": "document",
    "content": {
        "sections": parse_sections(page['body']),
        "attachments": page['attachments']
    },
    "source_type": "confluence",
    "source_id": page['id'],
    "source_url": page['url'],
    "last_synced": datetime.now().isoformat()
}).execute()
```

### Update Existing (UPSERT)
```python
# Check if exists
existing = supabase.table('knowledge_base')\
    .select('id')\
    .eq('question', question)\
    .eq('source_type', 'confluence')\
    .execute()

if existing.data:
    # Update
    supabase.table('knowledge_base')\
        .update({"answer": new_answer, "last_synced": datetime.now()})\
        .eq('id', existing.data[0]['id'])\
        .execute()
else:
    # Insert
    supabase.table('knowledge_base').insert({...}).execute()
```

---

## Field Limits

| Field | Limit | Notes |
|-------|-------|-------|
| `question` | No limit | TEXT field |
| `answer` | No limit | TEXT field |
| `content` | 1GB | JSONB (practical limit ~100MB) |
| `metadata` | 1GB | JSONB (practical limit ~100MB) |
| `tags` | 1000 items | Array (practical limit ~50) |
| `media_urls` | 1GB | JSONB (practical limit ~100 URLs) |

---

## Best Practices

### ✅ DO
- Use structured fields for common data
- Use JSONB for variable/custom data
- Add tags for easy filtering
- Set priority for important content
- Track source for sync operations
- Use content_type to categorize

### ❌ DON'T
- Put common data in JSONB (slower)
- Create columns for rare fields
- Store huge files in JSONB (use URLs)
- Forget to set last_synced
- Skip validation in application

---

## Content Type Reference

| Type | Use For | Example |
|------|---------|---------|
| `qa` | Simple Q&A | "What is X?" |
| `document` | Full documents | Confluence pages |
| `tutorial` | Step-by-step | "How to deploy" |
| `policy` | Company policies | "Vacation policy" |
| `faq` | Multiple Q&As | "Password reset FAQ" |
| `code` | Code snippets | Python examples |
| `troubleshooting` | Problem-solution | "Fix error X" |
| `reference` | Technical docs | API reference |
| `other` | Anything else | Custom types |

---

## Source Type Reference

| Type | Use For | ID Format |
|------|---------|-----------|
| `confluence` | Confluence pages | `page-12345` |
| `figma` | Figma designs | `file-abc123-node-456` |
| `github` | GitHub repos | `repo/path/file.py` |
| `jira` | Jira issues | `PROJ-123` |
| `notion` | Notion pages | `page-uuid` |
| `manual` | Manually added | `manual-001` |
| `api` | Via API | `api-request-id` |

---

## Need More Help?

- **Full Guide**: `docs/HYBRID_SCHEMA_GUIDE.md`
- **Examples**: `database/hybrid_examples.sql`
- **Schema**: `database/schema.sql`
- **Setup**: `docs/SUPABASE_SETUP.md`
