# 🏗️ Hybrid Schema Architecture

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID KNOWLEDGE BASE                         │
│                                                                  │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  STRUCTURED FIELDS   │    │    FLEXIBLE JSONB FIELDS     │  │
│  │  (Fast Queries)      │    │    (Any Structure)           │  │
│  ├──────────────────────┤    ├──────────────────────────────┤  │
│  │ • id                 │    │ • content (JSONB)            │  │
│  │ • question           │    │   - Full documents           │  │
│  │ • answer             │    │   - Code snippets            │  │
│  │ • category           │    │   - Step-by-step guides      │  │
│  │ • tags[]             │    │   - Tables, lists            │  │
│  │ • priority           │    │   - Nested structures        │  │
│  │ • source_type        │    │   - ANY custom data!         │  │
│  │ • source_id          │    │                              │  │
│  │ • media_url          │    │ • metadata (JSONB)           │  │
│  │ • content_type       │    │   - Custom fields            │  │
│  │ • department         │    │   - Evolving data            │  │
│  │ • status             │    │   - Integration data         │  │
│  │ • created_at         │    │   - ANYTHING!                │  │
│  │ • updated_at         │    │                              │  │
│  └──────────────────────┘    └──────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              14 PERFORMANCE INDEXES                       │  │
│  │  • Full-text search  • Category  • Tags  • Priority      │  │
│  │  • Source tracking   • Content   • Media • Status        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                        INPUT SOURCES                              │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│  Confluence  │    Figma     │   GitHub     │   Manual Entry    │
│   Pages      │   Designs    │   Code       │   Direct Input    │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬──────────┘
       │              │              │                │
       │              │              │                │
       ▼              ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP EXTRACTORS                                │
│  Parse & Structure content from various sources                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SMART SYNC ENGINE                             │
│  • Detect duplicates                                             │
│  • UPSERT logic (update existing, insert new)                   │
│  • Track source & sync time                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID DATABASE                               │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │   Structured   │  │     JSONB      │  │     JSONB       │  │
│  │     Fields     │  │    content     │  │    metadata     │  │
│  │                │  │                │  │                 │  │
│  │  question ─────┼──┼─► {           │  │  {              │  │
│  │  answer   ─────┼──┼─►   "steps":  │  │    "custom":    │  │
│  │  category      │  │    [...],     │  │    "fields",    │  │
│  │  tags[]        │  │    "code":    │  │    "any":       │  │
│  │  priority      │  │    "...",     │  │    "data"       │  │
│  │  source_type   │  │    "any":     │  │  }              │  │
│  │  ...           │  │    "structure"│  │                 │  │
│  │                │  │  }            │  │                 │  │
│  └────────────────┘  └────────────────┘  └─────────────────┘  │
│                                                                  │
│  All indexed for fast queries!                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API / CHATBOT                                 │
│  • Fast queries on structured fields                             │
│  • Flexible access to JSONB content                             │
│  • TF-IDF vectorization for semantic search                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Document Type Examples

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT TYPES SUPPORTED                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Q&A (Simple Chatbot)                                        │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ question: "What is AI?"                               │   │
│     │ answer: "Artificial Intelligence is..."              │   │
│     │ content_type: "qa"                                   │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  2. Full Document (Confluence)                                  │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ question: "Vacation Policy"                          │   │
│     │ answer: "See full policy"                            │   │
│     │ content: {                                           │   │
│     │   "sections": [...],                                 │   │
│     │   "effective_date": "2026-01-01"                     │   │
│     │ }                                                     │   │
│     │ source_type: "confluence"                            │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  3. Code Snippet (GitHub)                                       │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ question: "How to connect DB?"                       │   │
│     │ answer: "Use this code"                              │   │
│     │ content: {                                           │   │
│     │   "language": "python",                              │   │
│     │   "code": "from supabase import...",                 │   │
│     │   "dependencies": ["supabase"]                       │   │
│     │ }                                                     │   │
│     │ content_type: "code"                                 │   │
│     │ source_type: "github"                                │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  4. Tutorial (Step-by-Step)                                     │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ question: "How to deploy?"                           │   │
│     │ answer: "Follow these steps"                         │   │
│     │ content: {                                           │   │
│     │   "steps": [                                         │   │
│     │     {"number": 1, "action": "Build"},               │   │
│     │     {"number": 2, "action": "Deploy"}               │   │
│     │   ],                                                 │   │
│     │   "duration": "10 minutes"                           │   │
│     │ }                                                     │   │
│     │ content_type: "tutorial"                             │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  5. Troubleshooting Guide                                       │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ question: "Fix timeout error?"                       │   │
│     │ answer: "Follow troubleshooting"                     │   │
│     │ content: {                                           │   │
│     │   "problem": "Connection Timeout",                   │   │
│     │   "symptoms": [...],                                 │   │
│     │   "steps": [...]                                     │   │
│     │ }                                                     │   │
│     │ content_type: "troubleshooting"                      │   │
│     │ priority: 8                                          │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                  │
│  6. Custom Type (Anything!)                                     │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ question: "Your custom question"                     │   │
│     │ answer: "Your custom answer"                         │   │
│     │ content: {                                           │   │
│     │   "your_field": "your_value",                        │   │
│     │   "nested": {                                        │   │
│     │     "data": "structure"                              │   │
│     │   }                                                   │   │
│     │ }                                                     │   │
│     │ metadata: {                                          │   │
│     │   "anything": "you want"                             │   │
│     │ }                                                     │   │
│     └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Sync Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                    SMART SYNC PROCESS                             │
└──────────────────────────────────────────────────────────────────┘

1. EXTRACT from Source
   ┌─────────────────────────────────────────────┐
   │  Confluence Page / Figma Design / GitHub    │
   └────────────────┬────────────────────────────┘
                    │
                    ▼
2. PARSE & STRUCTURE
   ┌─────────────────────────────────────────────┐
   │  Convert to Q&A format                      │
   │  Extract metadata                           │
   │  Identify media                             │
   │  Structure content                          │
   └────────────────┬────────────────────────────┘
                    │
                    ▼
3. CHECK for DUPLICATES
   ┌─────────────────────────────────────────────┐
   │  Query: Does this question + source exist?  │
   └────────────────┬────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
    EXISTS?                NEW?
         │                     │
         ▼                     ▼
4a. UPDATE              4b. INSERT
   ┌──────────┐            ┌──────────┐
   │ Replace  │            │ Add new  │
   │ answer   │            │ entry    │
   │ Update   │            │          │
   │ metadata │            │          │
   │ Set      │            │          │
   │ last_    │            │          │
   │ synced   │            │          │
   └──────────┘            └──────────┘
         │                     │
         └──────────┬──────────┘
                    │
                    ▼
5. RESULT
   ┌─────────────────────────────────────────────┐
   │  ✅ Database updated                        │
   │  ✅ Old info replaced with new              │
   │  ✅ Source tracking maintained              │
   │  ✅ Sync timestamp recorded                 │
   └─────────────────────────────────────────────┘
```

---

## Query Performance

```
┌──────────────────────────────────────────────────────────────────┐
│                    INDEXED FIELDS (FAST)                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Structured Fields (Millisecond queries)                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • category          → B-tree index                         │ │
│  │ • tags[]            → GIN index                            │ │
│  │ • priority          → B-tree index (DESC)                  │ │
│  │ • source_type       → B-tree index                         │ │
│  │ • source_id         → B-tree index                         │ │
│  │ • content_type      → B-tree index                         │ │
│  │ • status            → B-tree index                         │ │
│  │ • department        → B-tree index                         │ │
│  │ • source_parent_id  → B-tree index                         │ │
│  │ • last_synced       → B-tree index                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Full-Text Search (Fast)                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • question + answer → GIN index (tsvector)                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  JSONB Fields (Fast)                                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • content           → GIN index                            │ │
│  │ • metadata          → GIN index                            │ │
│  │ • media_urls        → GIN index                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Result: Sub-second queries even with millions of entries!       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Benefits Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHY HYBRID SCHEMA?                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ FLEXIBILITY                                                 │
│     • Store ANY document type                                   │
│     • Add custom fields without schema changes                  │
│     • Support evolving data structures                          │
│                                                                  │
│  ✅ PERFORMANCE                                                 │
│     • Fast queries on indexed structured fields                 │
│     • Efficient full-text search                                │
│     • Optimized JSONB queries                                   │
│                                                                  │
│  ✅ MAINTAINABILITY                                             │
│     • No schema migrations for new fields                       │
│     • Easy to extend                                            │
│     • Backward compatible                                       │
│                                                                  │
│  ✅ SCALABILITY                                                 │
│     • Handles millions of entries                               │
│     • Efficient storage                                         │
│     • Supports complex queries                                  │
│                                                                  │
│  ✅ FUTURE-PROOF                                                │
│     • Add new document types anytime                            │
│     • Store evolving data structures                            │
│     • No breaking changes                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Real-World Example

```
User updates Confluence page: "How to raise laptop ticket"
Old URL: abc.com → New URL: xyz.com

┌─────────────────────────────────────────────────────────────────┐
│  BEFORE SYNC                                                     │
├─────────────────────────────────────────────────────────────────┤
│  question: "How to raise laptop ticket?"                        │
│  answer: "Visit abc.com and fill the form..."                  │
│  source_type: "confluence"                                      │
│  source_id: "page-12345"                                        │
│  last_synced: "2026-05-26"                                      │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ User runs: python sync_from_mcp.py
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  SYNC ENGINE                                                     │
│  1. Fetch latest from Confluence                                │
│  2. Detect: Same question + source exists                       │
│  3. UPDATE (not insert)                                         │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AFTER SYNC                                                      │
├─────────────────────────────────────────────────────────────────┤
│  question: "How to raise laptop ticket?"                        │
│  answer: "Visit xyz.com and fill the form..."  ← UPDATED!      │
│  source_type: "confluence"                                      │
│  source_id: "page-12345"                                        │
│  last_synced: "2026-05-27"  ← NEW TIMESTAMP                     │
└─────────────────────────────────────────────────────────────────┘

Result: Chatbot now only knows xyz.com (abc.com is gone!) ✅
```

---

## Summary

The **Hybrid Schema** gives you:

🎯 **One table** for all document types  
⚡ **Fast queries** via structured fields  
🔄 **Infinite flexibility** via JSONB  
🔍 **Full-text search** built-in  
📊 **14 indexes** for performance  
🔄 **Smart sync** with UPSERT  
🌳 **Hierarchical** content support  
🎨 **Rich media** support  
🔐 **Access control** ready  
📈 **Scales** to millions of entries  

**Store anything. Query everything. Scale infinitely.** 🚀
