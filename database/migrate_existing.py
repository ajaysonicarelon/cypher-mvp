#!/usr/bin/env python3
"""
Migrate existing hardcoded knowledge base to Supabase
This script takes the current KNOWLEDGE_BASE array from main_simple.py
and migrates it to the Supabase database with proper source tracking.
"""

import os
import sys
from datetime import datetime
from supabase import create_client, Client

# Add parent directory to path to import from main_simple
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_supabase_client() -> Client:
    """Initialize Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables required")
        print("\nSet them with:")
        print("  export SUPABASE_URL='https://your-project.supabase.co'")
        print("  export SUPABASE_KEY='your-anon-key'")
        sys.exit(1)
    
    return create_client(url, key)

def migrate_data():
    """Migrate existing knowledge base to Supabase"""
    
    print("🚀 Starting migration from main_simple.py to Supabase...")
    print()
    
    # Import the existing knowledge base
    try:
        from main_simple import KNOWLEDGE_BASE
        print(f"✅ Found {len(KNOWLEDGE_BASE)} entries in main_simple.py")
    except ImportError:
        print("❌ Error: Could not import KNOWLEDGE_BASE from main_simple.py")
        sys.exit(1)
    
    # Initialize Supabase
    print("🔌 Connecting to Supabase...")
    supabase = get_supabase_client()
    print("✅ Connected successfully!")
    print()
    
    # Migrate each entry
    migrated = 0
    skipped = 0
    errors = 0
    
    print("📦 Migrating entries...")
    print("-" * 60)
    
    for idx, entry in enumerate(KNOWLEDGE_BASE, 1):
        question = entry.get("question")
        answer = entry.get("answer")
        media_url = entry.get("media_url")
        
        try:
            # Check if entry already exists
            existing = supabase.table('knowledge_base')\
                .select('id')\
                .eq('question', question)\
                .eq('source_type', 'manual')\
                .execute()
            
            if existing.data:
                print(f"⏭️  [{idx}/{len(KNOWLEDGE_BASE)}] Skipped (already exists): {question[:50]}...")
                skipped += 1
                continue
            
            # Prepare data for insertion
            data = {
                'question': question,
                'answer': answer,
                'media_url': media_url,
                'source_type': 'manual',
                'source_id': f'migrated-{idx}',
                'category': 'ai-basics' if 'machine learning' in question.lower() or 'neural' in question.lower() else 'general',
                'tags': extract_tags(question, answer),
                'metadata': {
                    'migrated_from': 'main_simple.py',
                    'migration_date': datetime.now().isoformat(),
                    'has_media': media_url is not None
                },
                'last_synced': datetime.now().isoformat()
            }
            
            # Insert into Supabase
            result = supabase.table('knowledge_base').insert(data).execute()
            
            print(f"✅ [{idx}/{len(KNOWLEDGE_BASE)}] Migrated: {question[:50]}...")
            migrated += 1
            
        except Exception as e:
            print(f"❌ [{idx}/{len(KNOWLEDGE_BASE)}] Error: {question[:50]}...")
            print(f"   Error details: {str(e)}")
            errors += 1
    
    print("-" * 60)
    print()
    print("📊 Migration Summary:")
    print(f"   ✅ Migrated: {migrated}")
    print(f"   ⏭️  Skipped:  {skipped}")
    print(f"   ❌ Errors:   {errors}")
    print(f"   📦 Total:    {len(KNOWLEDGE_BASE)}")
    print()
    
    if migrated > 0:
        print("🎉 Migration completed successfully!")
        print()
        print("📝 Next steps:")
        print("   1. Verify data in Supabase dashboard")
        print("   2. Test API with: python database/test_connection.py")
        print("   3. Update your app to use Supabase instead of hardcoded data")
    else:
        print("ℹ️  No new entries to migrate")

def extract_tags(question: str, answer: str) -> list:
    """Extract relevant tags from question and answer"""
    text = (question + " " + answer).lower()
    
    tags = []
    
    # Common AI/ML terms
    keywords = {
        'machine learning': 'machine-learning',
        'neural network': 'neural-networks',
        'deep learning': 'deep-learning',
        'artificial intelligence': 'ai',
        'nlp': 'nlp',
        'natural language': 'nlp',
        'data science': 'data-science',
        'algorithm': 'algorithms',
        'model': 'models',
        'training': 'training',
        'architecture': 'architecture'
    }
    
    for keyword, tag in keywords.items():
        if keyword in text and tag not in tags:
            tags.append(tag)
    
    # Ensure at least one tag
    if not tags:
        tags.append('general')
    
    return tags

def verify_migration():
    """Verify the migration was successful"""
    print()
    print("🔍 Verifying migration...")
    
    supabase = get_supabase_client()
    
    # Get total count
    result = supabase.table('knowledge_base').select('*', count='exact').execute()
    total = result.count if hasattr(result, 'count') else len(result.data)
    
    print(f"✅ Total entries in database: {total}")
    
    # Get entries by source
    result = supabase.table('knowledge_base')\
        .select('source_type')\
        .execute()
    
    sources = {}
    for row in result.data:
        source = row.get('source_type', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print()
    print("📊 Entries by source:")
    for source, count in sources.items():
        print(f"   {source}: {count}")

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  Knowledge Base Migration Tool")
    print("  From: main_simple.py (hardcoded)")
    print("  To:   Supabase (PostgreSQL)")
    print("=" * 60)
    print()
    
    try:
        migrate_data()
        verify_migration()
    except KeyboardInterrupt:
        print()
        print("⚠️  Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)
