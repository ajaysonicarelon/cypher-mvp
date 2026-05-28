from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from typing import Optional
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="Local AI Chatbot with Supabase", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
supabase: Client = None
vectorizer = None
knowledge_vectors = None
knowledge_base_cache = []
CONFIDENCE_THRESHOLD = 0.40

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    confidence: float
    media_url: Optional[str] = None

@app.on_event("startup")
async def load_model():
    global vectorizer, knowledge_vectors, supabase, knowledge_base_cache
    
    print("🔌 Connecting to Supabase...")
    
    # Initialize Supabase
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY not set!")
        print("Please create .env file with your credentials")
        raise Exception("Supabase credentials not configured")
    
    supabase = create_client(url, key)
    print("✅ Connected to Supabase!")
    
    print("📥 Fetching knowledge base from Supabase...")
    
    # Fetch all active entries from Supabase
    try:
        result = supabase.table('knowledge_base')\
            .select('question, answer, media_url')\
            .eq('status', 'active')\
            .execute()
        
        knowledge_base_cache = result.data
        print(f"✅ Loaded {len(knowledge_base_cache)} entries from Supabase")
        
        if len(knowledge_base_cache) == 0:
            print("⚠️  Warning: No data in Supabase! Run seed_data.sql first.")
            return
        
    except Exception as e:
        print(f"❌ Error fetching from Supabase: {e}")
        raise
    
    print("🔧 Initializing TF-IDF vectorizer...")
    
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words='english',
        ngram_range=(1, 2),
        max_features=1000
    )
    
    print("📊 Pre-computing knowledge base vectors...")
    questions = [item["question"] for item in knowledge_base_cache]
    knowledge_vectors = vectorizer.fit_transform(questions)
    print(f"✅ Vectorized {len(knowledge_base_cache)} knowledge base entries.")
    print("🎉 System ready!")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if len(knowledge_base_cache) == 0:
        raise HTTPException(status_code=503, detail="Knowledge base not loaded. Please check server logs.")
    
    user_message = request.message.strip()
    
    # Vectorize user query
    user_vector = vectorizer.transform([user_message])
    
    # Calculate similarities
    similarities = sklearn_cosine_similarity(user_vector, knowledge_vectors)[0]
    
    # Find best match
    best_match_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_match_idx])
    
    # Check confidence threshold
    if best_score < CONFIDENCE_THRESHOLD:
        return ChatResponse(
            reply="I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
            confidence=best_score,
            media_url=None
        )
    
    # Get matched item
    matched_item = knowledge_base_cache[best_match_idx]
    
    return ChatResponse(
        reply=matched_item["answer"],
        confidence=best_score,
        media_url=matched_item.get("media_url")
    )

@app.get("/")
async def root():
    return {
        "message": "Local AI Chatbot API with Supabase",
        "model": "TF-IDF with scikit-learn",
        "data_source": "Supabase PostgreSQL",
        "knowledge_base_size": len(knowledge_base_cache),
        "confidence_threshold": CONFIDENCE_THRESHOLD
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "supabase_connected": supabase is not None,
        "vectorizer_loaded": vectorizer is not None,
        "vectors_ready": knowledge_vectors is not None,
        "entries_loaded": len(knowledge_base_cache)
    }

@app.get("/reload")
async def reload_knowledge_base():
    """Reload knowledge base from Supabase (useful after updates)"""
    global knowledge_base_cache, knowledge_vectors
    
    try:
        print("🔄 Reloading knowledge base from Supabase...")
        
        result = supabase.table('knowledge_base')\
            .select('question, answer, media_url')\
            .eq('status', 'active')\
            .execute()
        
        knowledge_base_cache = result.data
        
        # Re-vectorize
        questions = [item["question"] for item in knowledge_base_cache]
        knowledge_vectors = vectorizer.fit_transform(questions)
        
        print(f"✅ Reloaded {len(knowledge_base_cache)} entries")
        
        return {
            "status": "success",
            "entries_loaded": len(knowledge_base_cache),
            "message": "Knowledge base reloaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reload failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
