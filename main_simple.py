from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from typing import Optional
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

app = FastAPI(title="Local AI Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KNOWLEDGE_BASE = [
    {
        "question": "What is machine learning?",
        "answer": "Machine learning is a branch of artificial intelligence that enables computers to learn from data and improve their performance without being explicitly programmed. It uses algorithms to identify patterns and make decisions based on input data.",
        "media_url": None
    },
    {
        "question": "How do neural networks work?",
        "answer": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers that process information through weighted connections, learning to recognize patterns through training.",
        "media_url": None
    },
    {
        "question": "Show me a diagram of AI architecture",
        "answer": "Here's a visual representation of a typical AI system architecture showing the data flow from input through processing layers to output.",
        "media_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80"
    },
    {
        "question": "What does a data science workflow look like?",
        "answer": "A data science workflow typically includes data collection, cleaning, exploration, modeling, and deployment. Here's a visual guide to the process.",
        "media_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80"
    },
    {
        "question": "What is deep learning?",
        "answer": "Deep learning is a subset of machine learning that uses neural networks with multiple layers (deep neural networks) to progressively extract higher-level features from raw input. It excels at tasks like image recognition, natural language processing, and speech recognition.",
        "media_url": None
    },
    {
        "question": "Explain natural language processing",
        "answer": "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language. It enables machines to read, understand, and derive meaning from human languages, powering applications like chatbots, translation services, and sentiment analysis.",
        "media_url": None
    }
]

vectorizer = None
knowledge_vectors = None
CONFIDENCE_THRESHOLD = 0.40

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    confidence: float
    media_url: Optional[str] = None

@app.on_event("startup")
async def load_model():
    global vectorizer, knowledge_vectors
    print("Initializing TF-IDF vectorizer...")
    
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words='english',
        ngram_range=(1, 2),
        max_features=1000
    )
    
    print("Pre-computing knowledge base vectors...")
    questions = [item["question"] for item in KNOWLEDGE_BASE]
    knowledge_vectors = vectorizer.fit_transform(questions)
    print(f"Vectorized {len(KNOWLEDGE_BASE)} knowledge base entries.")
    print("System ready!")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    user_message = request.message.strip()
    
    user_vector = vectorizer.transform([user_message])
    
    similarities = sklearn_cosine_similarity(user_vector, knowledge_vectors)[0]
    
    best_match_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_match_idx])
    
    if best_score < CONFIDENCE_THRESHOLD:
        return ChatResponse(
            reply="I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
            confidence=best_score,
            media_url=None
        )
    
    matched_item = KNOWLEDGE_BASE[best_match_idx]
    
    return ChatResponse(
        reply=matched_item["answer"],
        confidence=best_score,
        media_url=matched_item["media_url"]
    )

@app.get("/")
async def root():
    return {
        "message": "Local AI Chatbot API is running",
        "model": "TF-IDF with scikit-learn",
        "knowledge_base_size": len(KNOWLEDGE_BASE),
        "confidence_threshold": CONFIDENCE_THRESHOLD
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "vectorizer_loaded": vectorizer is not None,
        "vectors_ready": knowledge_vectors is not None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
