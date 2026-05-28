"""
Flask API for Vercel Deployment
Handles chat and health endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from supabase import create_client

app = Flask(__name__)
CORS(app)

# Global variables for caching
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

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Chat endpoint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Initialize system
        initialize_system()
        
        # Get message
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Vectorize user query
        user_vector = _vectorizer.transform([message])
        
        # Calculate similarities
        similarities = sklearn_cosine_similarity(user_vector, _knowledge_vectors)[0]
        
        # Find best match
        best_match_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_match_idx])
        
        # Check confidence threshold
        if best_score < CONFIDENCE_THRESHOLD:
            return jsonify({
                'reply': "I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
                'confidence': best_score,
                'media_url': None
            })
        
        # Get matched item
        matched_item = _knowledge_base_cache[best_match_idx]
        
        return jsonify({
            'reply': matched_item['answer'],
            'confidence': best_score,
            'media_url': matched_item.get('media_url')
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    """Health check endpoint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Check environment variables
        supabase_url = os.environ.get('SUPABASE_URL', '')
        supabase_key = os.environ.get('SUPABASE_KEY', '')
        
        has_supabase_url = bool(supabase_url)
        has_supabase_key = bool(supabase_key)
        
        return jsonify({
            'status': 'healthy' if (has_supabase_url and has_supabase_key) else 'degraded',
            'environment': {
                'supabase_url_configured': has_supabase_url,
                'supabase_key_configured': has_supabase_key,
                'confidence_threshold': CONFIDENCE_THRESHOLD
            },
            'message': 'AI Chatbot API is running on Vercel',
            'version': '2.0.0'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/')
def index():
    """Serve the frontend"""
    try:
        # Try to serve from public directory
        return send_from_directory('../public', 'index.html')
    except:
        # Fallback to API info
        return jsonify({
            'message': 'AI Chatbot API',
            'endpoints': {
                'chat': '/api/chat (POST)',
                'health': '/api/health (GET)'
            }
        })

# For Vercel
if __name__ == '__main__':
    app.run()
