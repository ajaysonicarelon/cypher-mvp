#!/usr/bin/env python3
"""
Upload master onboarding checklist to Supabase
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

def upload_master_checklist():
    """Upload master onboarding checklist"""
    
    print("🚀 Starting master checklist upload...")
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connected to Supabase")
    
    # Read CSV file
    csv_file = 'master_onboarding_checklist.csv'
    
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
    
    print(f"📊 Found {len(data_to_insert)} master checklist items to upload")
    
    # Upload
    try:
        result = supabase.table('knowledge_base').insert(data_to_insert).execute()
        print(f"✅ Uploaded {len(data_to_insert)} master checklist items")
    except Exception as e:
        print(f"❌ Error uploading: {str(e)}")
        return
    
    # Verify total count
    try:
        result = supabase.table('knowledge_base').select('*').eq('category', 'onboarding').execute()
        print(f"✅ Verification: Total {len(result.data)} onboarding items in database")
    except Exception as e:
        print(f"⚠️ Verification failed: {str(e)}")

if __name__ == '__main__':
    upload_master_checklist()
