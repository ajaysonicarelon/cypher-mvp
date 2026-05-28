# 🗄️ Supabase Setup Guide

Complete guide to setting up your Supabase database for the AI Chatbot.

---

## 📋 Prerequisites

- Supabase account (free tier works perfectly)
- Python 3.10+ installed
- Basic SQL knowledge (helpful but not required)

---

## 🚀 Step-by-Step Setup

### Step 1: Create Supabase Project

1. **Go to [Supabase](https://supabase.com)**
2. **Sign up / Log in**
3. **Click "New Project"**
   - Organization: Select or create one
   - Name: `ai-chatbot` (or your preferred name)
   - Database Password: Generate a strong password (save it!)
   - Region: Choose closest to your users
   - Pricing Plan: Free tier is sufficient

4. **Wait for project to initialize** (~2 minutes)

---

### Step 2: Run Database Schema

1. **Open SQL Editor**
   - In your Supabase dashboard
   - Click "SQL Editor" in the left sidebar
   - Click "New Query"

2. **Copy schema.sql**
   ```bash
   cat database/schema.sql
   ```
   - Copy the entire contents
   - Paste into the SQL Editor

3. **Execute the query**
   - Click "Run" or press `Cmd/Ctrl + Enter`
   - You should see success messages

4. **Verify table creation**
   - Click "Table Editor" in sidebar
   - You should see `knowledge_base` table

---

### Step 3: Populate Initial Data

1. **Open SQL Editor again**
   - Click "New Query"

2. **Copy seed_data.sql**
   ```bash
   cat database/seed_data.sql
   ```
   - Copy the entire contents
   - Paste into the SQL Editor

3. **Execute the query**
   - Click "Run"
   - You should see 8 entries inserted

4. **Verify data**
   - Go to "Table Editor"
   - Click on `knowledge_base` table
   - You should see your Q&A entries

---

### Step 4: Get API Credentials

1. **Go to Project Settings**
   - Click the gear icon (⚙️) in sidebar
   - Click "API" section

2. **Copy these values:**
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: Long string starting with `eyJ...`

3. **Save them securely** (you'll need them next)

---

### Step 5: Configure Environment Variables

#### For Local Development

Create a `.env` file in the project root:

```bash
# In mvp/ directory
cat > .env << 'EOF'
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
EOF
```

**Replace with your actual values!**

#### For Vercel Deployment (Later)

You'll add these in the Vercel dashboard:
- Go to Project Settings → Environment Variables
- Add `SUPABASE_URL` and `SUPABASE_KEY`

---

### Step 6: Install Python Dependencies

```bash
# Install Supabase client
pip3 install supabase

# Or update requirements.txt
echo "supabase==2.3.0" >> requirements.txt
pip3 install -r requirements.txt
```

---

### Step 7: Test Connection

```bash
# Set environment variables (if not using .env file)
export SUPABASE_URL='https://your-project.supabase.co'
export SUPABASE_KEY='your-anon-key'

# Run test script
python3 database/test_connection.py
```

**Expected output:**
```
🔌 Testing Supabase connection...
✅ Connection successful!

📋 Checking if knowledge_base table exists...
✅ Table exists!

📖 Testing data read...
✅ Successfully read 5 entries

✍️  Testing data write...
✅ Write successful! (ID: 123)
✅ Test entry cleaned up

🔍 Testing search...
✅ Search successful! Found 3 entries matching 'machine'

🔄 Testing update (UPSERT)...
✅ Test entry created (ID: 124)
✅ Update successful!
✅ Update verified!
✅ Test entry cleaned up

📊 Database Statistics:
   Total entries: 8
   Entries by source:
      manual: 8
   Entries with media: 2

✅ All tests completed!
```

---

### Step 8: Migrate Existing Data (Optional)

If you have data in `main_simple.py` that you want to migrate:

```bash
python3 database/migrate_existing.py
```

This will:
- Read `KNOWLEDGE_BASE` from `main_simple.py`
- Insert entries into Supabase
- Skip duplicates
- Add source tracking

---

## 🔍 Verify Your Setup

### Check in Supabase Dashboard

1. **Table Editor**
   - Should see `knowledge_base` table
   - Should have 8+ entries

2. **SQL Editor - Run queries**
   ```sql
   -- Count total entries
   SELECT COUNT(*) FROM knowledge_base;
   
   -- View all entries
   SELECT question, source_type, category FROM knowledge_base;
   
   -- Search for specific content
   SELECT * FROM knowledge_base WHERE question ILIKE '%machine%';
   ```

3. **API Docs**
   - Click "API" in sidebar
   - See auto-generated REST endpoints
   - Test queries in the interactive docs

---

## 📊 Understanding the Schema

### Main Table: `knowledge_base`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Auto-increment primary key |
| `question` | TEXT | The question text |
| `answer` | TEXT | The answer text |
| `media_url` | TEXT | Optional image/video URL |
| `source_type` | TEXT | 'confluence', 'figma', 'manual', 'api' |
| `source_id` | TEXT | External ID (page ID, file key) |
| `source_url` | TEXT | Direct link to source |
| `last_synced` | TIMESTAMP | When last updated from source |
| `category` | TEXT | For filtering/organization |
| `tags` | TEXT[] | Array of tags |
| `metadata` | JSONB | Flexible JSON storage |
| `created_at` | TIMESTAMP | When entry was created |
| `updated_at` | TIMESTAMP | Auto-updated on changes |

### Indexes

- Full-text search on question + answer
- Source lookups (type + id)
- Category filtering
- Tag searches
- Metadata queries
- Last synced tracking

### Views

- `recent_syncs` - Recently updated entries
- `entries_by_source` - Count by source type

### Functions

- `search_knowledge_base(query)` - Full-text search
- `update_updated_at_column()` - Auto-update timestamp

---

## 🔐 Security Considerations

### Row Level Security (RLS)

Currently disabled for simplicity. To enable:

```sql
-- Enable RLS
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;

-- Allow public read
CREATE POLICY "Allow public read access"
ON knowledge_base FOR SELECT
USING (true);

-- Restrict writes to authenticated users
CREATE POLICY "Allow authenticated write"
ON knowledge_base FOR INSERT
WITH CHECK (auth.role() = 'authenticated');
```

### API Keys

- **anon/public key**: Safe to use in frontend (read-only by default)
- **service_role key**: NEVER expose! Server-side only, full access

---

## 🛠️ Common Operations

### Add New Entry via SQL

```sql
INSERT INTO knowledge_base (question, answer, source_type, category, tags)
VALUES (
    'Your question here?',
    'Your answer here',
    'manual',
    'general',
    ARRAY['tag1', 'tag2']
);
```

### Update Existing Entry

```sql
UPDATE knowledge_base
SET answer = 'Updated answer',
    last_synced = NOW()
WHERE question = 'Your question here?';
```

### Delete Entry

```sql
DELETE FROM knowledge_base
WHERE id = 123;
```

### Search Entries

```sql
-- Simple search
SELECT * FROM knowledge_base
WHERE question ILIKE '%machine learning%';

-- Full-text search
SELECT * FROM search_knowledge_base('neural networks');

-- Filter by source
SELECT * FROM knowledge_base
WHERE source_type = 'confluence';

-- Filter by tags
SELECT * FROM knowledge_base
WHERE 'ai' = ANY(tags);
```

---

## 🐛 Troubleshooting

### Connection Failed

**Problem**: Can't connect to Supabase

**Solutions**:
1. Check URL format: `https://xxxxx.supabase.co` (no trailing slash)
2. Verify API key is the anon/public key (not service_role)
3. Check if project is paused (free tier auto-pauses after inactivity)
4. Verify environment variables are set correctly

### Table Not Found

**Problem**: `relation "knowledge_base" does not exist`

**Solution**: Run `schema.sql` in SQL Editor

### Permission Denied

**Problem**: Can't insert/update data

**Solutions**:
1. Check if RLS is enabled (disable for testing)
2. Use service_role key for admin operations
3. Verify API key permissions

### Duplicate Key Error

**Problem**: `duplicate key value violates unique constraint`

**Solution**: Entry with same question + source_type already exists
- Either update existing entry
- Or change the question/source_type

---

## 📈 Monitoring & Maintenance

### Check Database Size

```sql
SELECT pg_size_pretty(pg_database_size(current_database()));
```

### View Recent Changes

```sql
SELECT * FROM recent_syncs LIMIT 10;
```

### Find Stale Entries

```sql
SELECT question, last_synced,
       NOW() - last_synced as age
FROM knowledge_base
WHERE last_synced < NOW() - INTERVAL '7 days'
ORDER BY last_synced;
```

### Backup Data

```sql
-- Export as JSON
SELECT json_agg(row_to_json(t))
FROM knowledge_base t;
```

---

## ✅ Checklist

Before moving to Phase 2, verify:

- [ ] Supabase project created
- [ ] `schema.sql` executed successfully
- [ ] `seed_data.sql` executed successfully
- [ ] API credentials obtained
- [ ] Environment variables configured
- [ ] `test_connection.py` passes all tests
- [ ] Can view data in Table Editor
- [ ] Can query data via SQL Editor

---

## 🎯 Next Steps

Once your Supabase is set up:

1. **Phase 2**: Restructure for Vercel deployment
2. **Phase 3**: Build MCP extractors for Confluence/Figma
3. **Phase 4**: Implement smart sync engine
4. **Phase 5**: Deploy to production

---

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [SQL Tutorial](https://www.postgresqltutorial.com/)

---

**Need help?** Check the troubleshooting section or review the test output for specific error messages.
