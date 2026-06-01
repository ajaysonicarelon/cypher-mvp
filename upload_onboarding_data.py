#!/usr/bin/env python3
"""
Upload onboarding seed data to Supabase knowledge_base table
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

def upload_onboarding_data():
    """Upload onboarding Q&A pairs to Supabase"""
    
    print("🚀 Starting onboarding data upload...")
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connected to Supabase")
    
    # Read CSV file
    csv_file = 'onboarding_seed_data.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found!")
        return
    
    # Read and parse CSV
    data_to_insert = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_to_insert.append({
                'question': row['question'],
                'answer': row['answer'],
                'category': row['category'],
                'status': row['status']
            })
    
    print(f"📊 Found {len(data_to_insert)} Q&A pairs to upload")
    
    # Upload in batches (Supabase has limits)
    batch_size = 50
    total_uploaded = 0
    
    for i in range(0, len(data_to_insert), batch_size):
        batch = data_to_insert[i:i + batch_size]
        
        try:
            result = supabase.table('knowledge_base').insert(batch).execute()
            total_uploaded += len(batch)
            print(f"✅ Uploaded batch {i//batch_size + 1}: {len(batch)} items (Total: {total_uploaded}/{len(data_to_insert)})")
        except Exception as e:
            print(f"❌ Error uploading batch {i//batch_size + 1}: {str(e)}")
            print(f"   Batch data: {batch[0] if batch else 'empty'}")
    
    print(f"\n🎉 Upload complete! Total uploaded: {total_uploaded}/{len(data_to_insert)}")
    
    # Verify upload
    try:
        result = supabase.table('knowledge_base').select('*').eq('category', 'onboarding').execute()
        print(f"✅ Verification: Found {len(result.data)} onboarding items in database")
    except Exception as e:
        print(f"⚠️ Verification failed: {str(e)}")

if __name__ == '__main__':
    upload_onboarding_data()
