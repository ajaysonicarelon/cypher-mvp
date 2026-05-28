"""
Netlify Serverless Function: Chat Endpoint
"""
import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from supabase import create_client

# Global cache
_supabase = None
_vectorizer = None
_knowledge_vectors = None
_knowledge_base_cache = []
_initialized = False

CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.40'))

def get_supabase():
    global _supabase
    if _supabase is None:
        print("🔌 Creating Supabase client...")
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        print(f"🔑 SUPABASE_URL configured: {bool(url)}")
        print(f"🔑 SUPABASE_KEY configured: {bool(key)}")
        if not url or not key:
            raise Exception('SUPABASE_URL and SUPABASE_KEY must be set')
        _supabase = create_client(url, key)
        print("✅ Supabase client created")
    return _supabase

def initialize_system():
    global _vectorizer, _knowledge_vectors, _knowledge_base_cache, _initialized
    if _initialized:
        print("✅ System already initialized")
        return
    
    print("🔌 Initializing system...")
    supabase = get_supabase()
    print("📊 Fetching knowledge base from Supabase...")
    result = supabase.table('knowledge_base').select('question, answer, media_url').eq('status', 'active').execute()
    _knowledge_base_cache = result.data
    print(f"✅ Loaded {len(_knowledge_base_cache)} knowledge base entries")
    
    print("🤖 Creating TF-IDF vectorizer...")
    _vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2), max_features=1000)
    questions = [item["question"] for item in _knowledge_base_cache]
    print("🔢 Fitting vectorizer...")
    _knowledge_vectors = _vectorizer.fit_transform(questions)
    _initialized = True
    print("✅ System initialization complete")

def handler(event, context):
    """Netlify function handler"""
    
    print("🚀 Chat function called")
    print(f"📥 HTTP Method: {event.get('httpMethod')}")
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS
    if event['httpMethod'] == 'OPTIONS':
        print("✅ OPTIONS request handled")
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        print("🔄 Initializing system...")
        initialize_system()
        print("✅ System initialized")
        
        body = json.loads(event['body'])
        message = body.get('message', '').strip()
        print(f"📝 Message received: {message}")
        
        if not message:
            print("❌ Empty message")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Message cannot be empty'})
            }
        
        print("🔍 Vectorizing message...")
        user_vector = _vectorizer.transform([message])
        print("🔍 Computing similarities...")
        similarities = sklearn_cosine_similarity(user_vector, _knowledge_vectors)[0]
        best_match_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_match_idx])
        print(f"📊 Best match score: {best_score}")
        
        if best_score < CONFIDENCE_THRESHOLD:
            print(f"⚠️ Low confidence ({best_score} < {CONFIDENCE_THRESHOLD})")
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'reply': "I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
                    'confidence': best_score,
                    'media_url': None
                })
            }
        
        matched_item = _knowledge_base_cache[best_match_idx]
        print(f"✅ Matched answer: {matched_item['answer'][:50]}...")
        
        response_data = {
            'reply': matched_item['answer'],
            'confidence': best_score,
            'media_url': matched_item.get('media_url')
        }
        print(f"📤 Sending response: confidence={best_score}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
