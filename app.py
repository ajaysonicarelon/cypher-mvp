"""
Flask API for AI Chatbot - Render Deployment
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from supabase import create_client

app = Flask(__name__)
CORS(app)

# Global cache
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
    """Initialize vectorizer and load knowledge base"""
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

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    print("🏥 Health check called")
    
    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_key = os.environ.get('SUPABASE_KEY', '')
    
    return jsonify({
        'status': 'healthy' if (supabase_url and supabase_key) else 'degraded',
        'environment': {
            'supabase_url_configured': bool(supabase_url),
            'supabase_key_configured': bool(supabase_key),
            'confidence_threshold': CONFIDENCE_THRESHOLD
        },
        'message': 'AI Chatbot API is running on Render',
        'version': '2.0.0'
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Chat endpoint"""
    print("🚀 Chat endpoint called")
    print(f"📥 HTTP Method: {request.method}")
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        print("✅ OPTIONS request handled")
        return '', 200
    
    try:
        print("🔄 Initializing system...")
        initialize_system()
        print("✅ System initialized")
        
        data = request.get_json()
        message = data.get('message', '').strip()
        print(f"📝 Message received: {message}")
        
        if not message:
            print("❌ Empty message")
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        print("🔍 Vectorizing message...")
        user_vector = _vectorizer.transform([message])
        print("🔍 Computing similarities...")
        similarities = sklearn_cosine_similarity(user_vector, _knowledge_vectors)[0]
        best_match_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_match_idx])
        print(f"📊 Best match score: {best_score}")
        
        if best_score < CONFIDENCE_THRESHOLD:
            print(f"⚠️ Low confidence ({best_score} < {CONFIDENCE_THRESHOLD})")
            return jsonify({
                'reply': "I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
                'confidence': best_score,
                'media_url': None
            })
        
        matched_item = _knowledge_base_cache[best_match_idx]
        print(f"✅ Matched answer: {matched_item['answer'][:50]}...")
        
        response_data = {
            'reply': matched_item['answer'],
            'confidence': best_score,
            'media_url': matched_item.get('media_url')
        }
        print(f"📤 Sending response: confidence={best_score}")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'AI Chatbot API',
        'endpoints': {
            'health': '/health (GET)',
            'chat': '/chat (POST)'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
