#!/usr/bin/env python3
"""
Test Supabase connection and basic operations
Run this to verify your Supabase setup is working correctly
"""

import os
import sys
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_connection():
    """Test basic Supabase connection"""
    print("🔌 Testing Supabase connection...")
    
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Error: Environment variables not set")
        print("\nPlease set:")
        print("  export SUPABASE_URL='https://your-project.supabase.co'")
        print("  export SUPABASE_KEY='your-anon-key'")
        return False
    
    try:
        supabase = create_client(url, key)
        print("✅ Connection successful!")
        return supabase
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return None

def test_table_exists(supabase: Client):
    """Test if knowledge_base table exists"""
    print("\n📋 Checking if knowledge_base table exists...")
    
    try:
        result = supabase.table('knowledge_base').select('id').limit(1).execute()
        print("✅ Table exists!")
        return True
    except Exception as e:
        print(f"❌ Table not found: {str(e)}")
        print("\n📝 Please run schema.sql first:")
        print("   1. Go to Supabase dashboard")
        print("   2. Open SQL Editor")
        print("   3. Paste contents of database/schema.sql")
        print("   4. Execute the query")
        return False

def test_read_data(supabase: Client):
    """Test reading data from the table"""
    print("\n📖 Testing data read...")
    
    try:
        result = supabase.table('knowledge_base').select('*').limit(5).execute()
        count = len(result.data)
        
        if count > 0:
            print(f"✅ Successfully read {count} entries")
            print("\n📄 Sample entries:")
            for idx, entry in enumerate(result.data[:3], 1):
                question = entry.get('question', 'N/A')
                source = entry.get('source_type', 'N/A')
                print(f"   {idx}. {question[:60]}... (source: {source})")
            return True
        else:
            print("⚠️  Table is empty")
            print("\n📝 Run seed_data.sql to populate initial data:")
            print("   1. Go to Supabase dashboard")
            print("   2. Open SQL Editor")
            print("   3. Paste contents of database/seed_data.sql")
            print("   4. Execute the query")
            return False
    except Exception as e:
        print(f"❌ Read failed: {str(e)}")
        return False

def test_write_data(supabase: Client):
    """Test writing data to the table"""
    print("\n✍️  Testing data write...")
    
    test_entry = {
        'question': f'Test question at {datetime.now().isoformat()}',
        'answer': 'This is a test answer to verify write operations work correctly.',
        'source_type': 'manual',
        'source_id': 'test-connection',
        'category': 'test',
        'tags': ['test', 'connection'],
        'metadata': {'test': True, 'timestamp': datetime.now().isoformat()},
        'last_synced': datetime.now().isoformat()
    }
    
    try:
        result = supabase.table('knowledge_base').insert(test_entry).execute()
        
        if result.data:
            inserted_id = result.data[0].get('id')
            print(f"✅ Write successful! (ID: {inserted_id})")
            
            # Clean up test entry
            supabase.table('knowledge_base').delete().eq('id', inserted_id).execute()
            print("✅ Test entry cleaned up")
            return True
        else:
            print("⚠️  Write returned no data")
            return False
    except Exception as e:
        print(f"❌ Write failed: {str(e)}")
        return False

def test_search(supabase: Client):
    """Test search functionality"""
    print("\n🔍 Testing search...")
    
    try:
        # Search for entries containing "machine learning"
        result = supabase.table('knowledge_base')\
            .select('question, answer')\
            .ilike('question', '%machine%')\
            .execute()
        
        count = len(result.data)
        print(f"✅ Search successful! Found {count} entries matching 'machine'")
        
        if count > 0:
            print("\n📄 Search results:")
            for idx, entry in enumerate(result.data[:3], 1):
                print(f"   {idx}. {entry.get('question', 'N/A')[:60]}...")
        
        return True
    except Exception as e:
        print(f"❌ Search failed: {str(e)}")
        return False

def test_update(supabase: Client):
    """Test update functionality"""
    print("\n🔄 Testing update (UPSERT)...")
    
    # First, insert a test entry
    test_question = f"Test update question {datetime.now().timestamp()}"
    
    try:
        # Insert
        insert_result = supabase.table('knowledge_base').insert({
            'question': test_question,
            'answer': 'Original answer',
            'source_type': 'manual',
            'source_id': 'test-update',
            'last_synced': datetime.now().isoformat()
        }).execute()
        
        entry_id = insert_result.data[0].get('id')
        print(f"✅ Test entry created (ID: {entry_id})")
        
        # Update
        update_result = supabase.table('knowledge_base')\
            .update({'answer': 'Updated answer'})\
            .eq('id', entry_id)\
            .execute()
        
        print("✅ Update successful!")
        
        # Verify update
        verify_result = supabase.table('knowledge_base')\
            .select('answer')\
            .eq('id', entry_id)\
            .execute()
        
        if verify_result.data[0].get('answer') == 'Updated answer':
            print("✅ Update verified!")
        
        # Clean up
        supabase.table('knowledge_base').delete().eq('id', entry_id).execute()
        print("✅ Test entry cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ Update test failed: {str(e)}")
        return False

def show_statistics(supabase: Client):
    """Show database statistics"""
    print("\n📊 Database Statistics:")
    print("-" * 60)
    
    try:
        # Total entries
        result = supabase.table('knowledge_base').select('*', count='exact').execute()
        total = result.count if hasattr(result, 'count') else len(result.data)
        print(f"   Total entries: {total}")
        
        # Entries by source
        result = supabase.table('knowledge_base').select('source_type').execute()
        sources = {}
        for row in result.data:
            source = row.get('source_type', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\n   Entries by source:")
        for source, count in sources.items():
            print(f"      {source}: {count}")
        
        # Entries with media
        result = supabase.table('knowledge_base')\
            .select('media_url')\
            .not_.is_('media_url', 'null')\
            .execute()
        media_count = len(result.data)
        print(f"\n   Entries with media: {media_count}")
        
        print("-" * 60)
        
    except Exception as e:
        print(f"   ⚠️  Could not fetch statistics: {str(e)}")

def main():
    print()
    print("=" * 60)
    print("  Supabase Connection Test Suite")
    print("=" * 60)
    print()
    
    # Test 1: Connection
    supabase = test_connection()
    if not supabase:
        sys.exit(1)
    
    # Test 2: Table exists
    if not test_table_exists(supabase):
        sys.exit(1)
    
    # Test 3: Read data
    test_read_data(supabase)
    
    # Test 4: Write data
    test_write_data(supabase)
    
    # Test 5: Search
    test_search(supabase)
    
    # Test 6: Update
    test_update(supabase)
    
    # Show statistics
    show_statistics(supabase)
    
    print()
    print("=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print()
    print("📝 Your Supabase setup is working correctly!")
    print()
    print("Next steps:")
    print("   1. Run migration: python database/migrate_existing.py")
    print("   2. Set up MCP extractors for Confluence/Figma")
    print("   3. Configure Vercel deployment")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {str(e)}")
        sys.exit(1)
