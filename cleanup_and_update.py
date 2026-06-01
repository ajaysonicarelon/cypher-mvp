#!/usr/bin/env python3
"""
Cleanup duplicate master checklist entries and upload new consolidated version
"""

import csv
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://hlfwxqyjvslvukkqgpvf.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsZnd4cXlqdnNsdnVra3FncHZmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk4OTE2NDksImV4cCI6MjA5NTQ2NzY0OX0.raD3fPzNuyf1q-zuJMvkETfcgEUXPlVvTQyuVlCsVfY')

def cleanup_and_update():
    """Delete old duplicate entries and upload new consolidated version"""
    
    print("🚀 Starting cleanup and update...")
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connected to Supabase")
    
    # Step 1: Delete old master checklist entries
    questions_to_delete = [
        "What is the complete onboarding checklist?",
        "Show me the complete onboarding flow",
        "Give me the full onboarding guide",
        "What do I need to do as a new UX designer?",
        "Show me all onboarding steps",
        "What is the onboarding process for new joiners?"
    ]
    
    print(f"\n🗑️  Deleting {len(questions_to_delete)} old duplicate entries...")
    deleted_count = 0
    
    for question in questions_to_delete:
        try:
            result = supabase.table('knowledge_base').delete().eq('question', question).execute()
            deleted_count += 1
            print(f"  ✅ Deleted: {question[:50]}...")
        except Exception as e:
            print(f"  ⚠️  Error deleting '{question}': {str(e)}")
    
    print(f"✅ Deleted {deleted_count} duplicate entries")
    
    # Step 2: Upload new consolidated entry
    print("\n📤 Uploading new consolidated entry...")
    
    csv_file = 'master_onboarding_checklist.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        return
    
    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    if len(data) == 0:
        print("❌ No data found in CSV")
        return
    
    print(f"📊 Found {len(data)} entry to upload")
    
    # Upload
    try:
        result = supabase.table('knowledge_base').insert(data).execute()
        print(f"✅ Uploaded consolidated entry with {len(data[0]['question'].split('|'))} question variations")
    except Exception as e:
        print(f"❌ Error uploading: {str(e)}")
        return
    
    # Verify
    try:
        result = supabase.table('knowledge_base').select('*').eq('category', 'onboarding').execute()
        print(f"\n✅ Verification: Total {len(result.data)} onboarding items in database")
        print(f"   (Reduced from 101 to {len(result.data)} by consolidating duplicates)")
    except Exception as e:
        print(f"⚠️ Verification failed: {str(e)}")

if __name__ == '__main__':
    cleanup_and_update()
