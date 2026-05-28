# 🗄️ Database - Hybrid Schema

## What is This?

A **hybrid database schema** that combines:
- **Structured fields** (for fast queries)
- **JSONB fields** (for flexible content)

This means you can store **ANY type of document** while maintaining performance!

---

## 📁 Files in This Directory

### Core Schema
- **`schema.sql`** - Main database schema (run this first!)
- **`seed_data.sql`** - Initial sample data
- **`hybrid_examples.sql`** - 10+ examples of different document types

### Python Scripts
- **`test_connection.py`** - Test your Supabase connection
- **`migrate_existing.py`** - Migrate data from main_simple.py

---

## 🚀 Quick Start

### 1. Create Supabase Project
Go to https://supabase.com and create a new project

### 2. Run Schema
```sql
-- In Supabase SQL Editor, run:
schema.sql
```

### 3. Add Sample Data
```sql
-- Then run:
seed_data.sql
```

### 4. Test Connection
```bash
export SUPABASE_URL='your-url'
export SUPABASE_KEY='your-key'
python3 test_connection.py
```

---

## 💡 What Can You Store?

| Type | Example |
|------|---------|
| **Q&A** | Simple chatbot responses |
| **Documents** | Full Confluence pages |
| **Code** | GitHub snippets |
| **Tutorials** | Step-by-step guides |
| **Policies** | HR policies, procedures |
| **Troubleshooting** | Problem-solution guides |
| **API Docs** | Reference documentation |
| **Custom** | Literally anything! |

---

## 📊 Schema Overview

### Required Fields
```sql
question    TEXT      -- The question/title
answer      TEXT      -- The answer/summary
```

### Optional Structured Fields
```sql
media_url       TEXT      -- Image, video, PDF
content_type    TEXT      -- qa, tutorial, code, etc.
category        TEXT      -- Main category
tags            TEXT[]    -- Array of tags
priority        INTEGER   -- Importance (0-10)
source_type     TEXT      -- confluence, figma, github
source_id       TEXT      -- External ID
```

### Flexible JSONB Fields
```sql
content         JSONB     -- ANY structured content
metadata        JSONB     -- ANY custom data
```

---

## 🔍 Example Queries

### Simple Q&A
```sql
SELECT * FROM knowledge_base WHERE content_type = 'qa';
```

### From Confluence
```sql
SELECT * FROM knowledge_base WHERE source_type = 'confluence';
```

### High Priority
```sql
SELECT * FROM knowledge_base WHERE priority >= 8;
```

### Python Code Examples
```sql
SELECT * FROM knowledge_base 
WHERE content_type = 'code' 
AND content->>'language' = 'python';
```

---

## 📚 Documentation

- **`docs/HYBRID_SCHEMA_GUIDE.md`** - Complete guide
- **`docs/HYBRID_QUICK_REFERENCE.md`** - Quick reference
- **`docs/HYBRID_ARCHITECTURE.md`** - Visual diagrams
- **`docs/SUPABASE_SETUP.md`** - Setup instructions

---

## ✅ Features

- ✅ Store ANY document type
- ✅ Fast queries (14 indexes)
- ✅ Full-text search
- ✅ Hierarchical content
- ✅ Multiple media support
- ✅ Source tracking
- ✅ Smart sync (UPSERT)
- ✅ Access control ready
- ✅ Scales to millions

---

## 🎯 Next Steps

1. ✅ Run `schema.sql` in Supabase
2. ✅ Run `seed_data.sql` for sample data
3. ✅ Test with `test_connection.py`
4. ✅ See `hybrid_examples.sql` for usage
5. ✅ Read `docs/HYBRID_SCHEMA_GUIDE.md`
6. 🚀 Start syncing from Confluence/Figma!

---

**Questions?** Check the docs folder for detailed guides!
