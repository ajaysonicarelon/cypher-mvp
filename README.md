# Local AI Chatbot with Semantic Search

A lightweight, production-ready AI chatbot that runs completely free without paid API keys. Uses local semantic search with the `all-MiniLM-L6-v2` model to match user questions against a pre-loaded knowledge base.

## 🚀 Features

- **100% Free**: No OpenAI, Anthropic, or any paid API keys required
- **Local Processing**: All ML inference runs on your machine using sentence-transformers
- **Semantic Search**: Uses cosine similarity to find the best matching answers
- **Confidence Threshold**: Only responds when confidence score ≥ 0.40
- **Media Support**: Can display images in chat responses
- **Modern UI**: Beautiful, responsive chat interface with typing indicators
- **Fast API**: Built with FastAPI for high-performance async operations

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Modern web browser

## 🛠️ Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sentence-transformers` - ML model library
- `numpy` - Numerical computing
- `pydantic` - Data validation

### Step 2: Start the Backend Server

**Option A: Quick Start (Recommended)**
```bash
./start.sh
```

This will automatically install dependencies, start the server, and open the frontend.

**Option B: Manual Start**
```bash
python3 main_simple.py
```

The system will:
1. Initialize the TF-IDF vectorizer
2. Pre-compute vectors for the knowledge base
3. Start the API server on `http://localhost:8000`

You should see output like:
```
Initializing TF-IDF vectorizer...
Pre-computing knowledge base vectors...
Vectorized 6 knowledge base entries.
System ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Note**: The original `main.py` uses sentence-transformers with the `all-MiniLM-L6-v2` model, but requires downloading from HuggingFace. The `main_simple.py` version uses TF-IDF with scikit-learn for instant startup with no downloads required.

### Step 3: Open the Frontend

Simply open `index.html` in your web browser:
- **macOS**: `open index.html`
- **Windows**: Double-click `index.html`
- **Linux**: `xdg-open index.html`

Or drag and drop the file into your browser.

## 💬 Usage

1. Type your question in the input field
2. Click "Send" or press Enter
3. The system will:
   - Convert your question to a vector embedding
   - Compare it against all knowledge base entries
   - Return the best match if confidence ≥ 0.40
   - Display images if the response includes media

### Example Questions

Try asking:
- "What is machine learning?"
- "How do neural networks work?"
- "Show me a diagram of AI architecture"
- "What does a data science workflow look like?"
- "Explain deep learning"
- "What is NLP?"

## 🔧 Architecture

### Backend (`main.py`)
- **Framework**: FastAPI with full CORS support
- **ML Model**: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- **Similarity**: Cosine similarity using NumPy
- **Threshold**: 0.40 minimum confidence score
- **Endpoints**:
  - `POST /chat` - Main chat endpoint
  - `GET /` - API info
  - `GET /health` - Health check

### Frontend (`index.html`)
- **Pure HTML/CSS/JS**: No frameworks or build tools
- **Responsive Design**: Works on desktop and mobile
- **Features**:
  - Smooth animations
  - Typing indicators
  - Image rendering
  - Confidence badges
  - Error handling
  - Auto-scroll

### Knowledge Base
The system includes 6 pre-loaded Q&A pairs covering:
- Machine Learning basics
- Neural Networks
- Deep Learning
- Natural Language Processing
- AI Architecture (with image)
- Data Science Workflow (with image)

## 🎨 Customization

### Adding New Knowledge

Edit the `KNOWLEDGE_BASE` list in `main.py`:

```python
KNOWLEDGE_BASE = [
    {
        "question": "Your question here",
        "answer": "Your answer here",
        "media_url": None  # or "https://example.com/image.jpg"
    },
    # Add more entries...
]
```

After adding entries, restart the server to recompute embeddings.

### Adjusting Confidence Threshold

Change the `CONFIDENCE_THRESHOLD` value in `main.py`:

```python
CONFIDENCE_THRESHOLD = 0.40  # Lower = more lenient, Higher = stricter
```

### Styling the UI

Modify the `<style>` section in `index.html` to customize:
- Colors and gradients
- Fonts and sizes
- Border radius and shadows
- Animations and transitions

## 🧪 Testing

### Test the API directly:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'
```

### Check API health:

```bash
curl http://localhost:8000/health
```

## 📊 Technical Details

- **Model Size**: ~90MB (downloads automatically)
- **Embedding Dimension**: 384
- **Inference Speed**: ~10-50ms per query (CPU)
- **Memory Usage**: ~500MB (model + embeddings)
- **Similarity Metric**: Cosine similarity
- **API Response Time**: <100ms typical

## 🔒 Security Notes

- CORS is enabled for all origins (`allow_origins=["*"]`)
- For production, restrict CORS to specific domains
- No authentication is implemented
- Input validation is handled by Pydantic

## 🐛 Troubleshooting

### Model won't download
- Check internet connection
- Ensure sufficient disk space (~100MB)
- Try manually: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"`

### Frontend can't connect
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Ensure `http://localhost:8000` is accessible

### Low confidence scores
- Questions must be semantically similar to knowledge base
- Try rephrasing your question
- Add more relevant entries to knowledge base
- Lower the confidence threshold (not recommended)

## 📝 License

This project is open source and available for any use.

## 🤝 Contributing

To extend this chatbot:
1. Add more knowledge base entries
2. Implement conversation history
3. Add user authentication
4. Deploy to cloud platforms
5. Integrate with databases
6. Add voice input/output

## 🎯 Performance Tips

- Pre-compute embeddings at startup (already implemented)
- Use GPU if available (modify model loading)
- Batch process multiple queries
- Cache frequent queries
- Implement vector database for large knowledge bases

---

**Built with ❤️ using FastAPI, sentence-transformers, and vanilla JavaScript**
