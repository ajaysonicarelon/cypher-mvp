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
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        _supabase = create_client(url, key)
    return _supabase

def initialize_system():
    global _vectorizer, _knowledge_vectors, _knowledge_base_cache, _initialized
    if _initialized:
        return
    
    supabase = get_supabase()
    result = supabase.table('knowledge_base').select('question, answer, media_url').eq('status', 'active').execute()
    _knowledge_base_cache = result.data
    
    _vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2), max_features=1000)
    questions = [item["question"] for item in _knowledge_base_cache]
    _knowledge_vectors = _vectorizer.fit_transform(questions)
    _initialized = True

def handler(event, context):
    """Netlify function handler"""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS
    if event['httpMethod'] == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        initialize_system()
        
        body = json.loads(event['body'])
        message = body.get('message', '').strip()
        
        if not message:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Message cannot be empty'})
            }
        
        user_vector = _vectorizer.transform([message])
        similarities = sklearn_cosine_similarity(user_vector, _knowledge_vectors)[0]
        best_match_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_match_idx])
        
        if best_score < CONFIDENCE_THRESHOLD:
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
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'reply': matched_item['answer'],
                'confidence': best_score,
                'media_url': matched_item.get('media_url')
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
