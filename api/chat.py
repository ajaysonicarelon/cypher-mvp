"""
Vercel Serverless Function: Chat Endpoint
Handles chat requests with Supabase knowledge base
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from supabase import create_client

# Global variables for caching (persists across warm starts)
_supabase = None
_vectorizer = None
_knowledge_vectors = None
_knowledge_base_cache = []
_initialized = False

CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.40'))

def get_supabase():
    """Get or create Supabase client"""
    global _supabase
    if _supabase is None:
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        if not url or not key:
            raise Exception('SUPABASE_URL and SUPABASE_KEY must be set')
        _supabase = create_client(url, key)
    return _supabase

def initialize_system():
    """Initialize vectorizer and load knowledge base"""
    global _vectorizer, _knowledge_vectors, _knowledge_base_cache, _initialized
    
    if _initialized:
        return
    
    print("🔌 Initializing system...")
    
    # Get Supabase client
    supabase = get_supabase()
    
    # Fetch knowledge base
    print("📥 Fetching knowledge base from Supabase...")
    result = supabase.table('knowledge_base')\
        .select('question, answer, media_url')\
        .eq('status', 'active')\
        .execute()
    
    _knowledge_base_cache = result.data
    print(f"✅ Loaded {len(_knowledge_base_cache)} entries")
    
    if len(_knowledge_base_cache) == 0:
        raise Exception("No data in knowledge base")
    
    # Initialize vectorizer
    print("🔧 Initializing TF-IDF vectorizer...")
    _vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words='english',
        ngram_range=(1, 2),
        max_features=1000
    )
    
    # Vectorize questions
    questions = [item["question"] for item in _knowledge_base_cache]
    _knowledge_vectors = _vectorizer.fit_transform(questions)
    print(f"✅ Vectorized {len(_knowledge_base_cache)} entries")
    
    _initialized = True
    print("🎉 System ready!")

def process_chat(message: str):
    """Process chat message and return response"""
    # Ensure system is initialized
    initialize_system()
    
    if not message or not message.strip():
        return {
            'error': 'Message cannot be empty',
            'status': 400
        }
    
    user_message = message.strip()
    
    # Vectorize user query
    user_vector = _vectorizer.transform([user_message])
    
    # Calculate similarities
    similarities = sklearn_cosine_similarity(user_vector, _knowledge_vectors)[0]
    
    # Find best match
    best_match_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_match_idx])
    
    # Check confidence threshold
    if best_score < CONFIDENCE_THRESHOLD:
        return {
            'reply': "I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
            'confidence': best_score,
            'media_url': None
        }
    
    # Get matched item
    matched_item = _knowledge_base_cache[best_match_idx]
    
    return {
        'reply': matched_item['answer'],
        'confidence': best_score,
        'media_url': matched_item.get('media_url')
    }

class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            # Get message
            message = data.get('message', '')
            
            # Process chat
            response = process_chat(message)
            
            # Check for error
            if 'error' in response:
                self.send_response(response.get('status', 400))
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': response['error']}).encode())
                return
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'Internal server error: {str(e)}'
            }).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests (CORS preflight)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
