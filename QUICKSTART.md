# 🚀 Quick Start Guide

## ⚡ Fastest Way to Run

```bash
./start.sh
```

That's it! The script will:
1. ✅ Install all dependencies
2. ✅ Start the backend server
3. ✅ Open the chat UI in your browser

## 📱 What You'll See

### Backend Terminal
```
🚀 Starting Local AI Chatbot...
📦 Checking dependencies...
✅ Python 3 found
🔧 Installing/updating dependencies...
🤖 Starting backend server...
   API will be available at: http://localhost:8000

Initializing TF-IDF vectorizer...
Pre-computing knowledge base vectors...
Vectorized 6 knowledge base entries.
System ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Browser Window
A beautiful chat interface will open automatically where you can start chatting immediately!

## 💬 Try These Questions

1. **"What is machine learning?"**
   - Get a detailed explanation of ML concepts

2. **"How do neural networks work?"**
   - Learn about neural network architecture

3. **"Show me a diagram of AI architecture"**
   - Receive an answer with an embedded image

4. **"What is deep learning?"**
   - Understand deep learning fundamentals

5. **"Explain natural language processing"**
   - Learn about NLP and its applications

## 🛑 To Stop the Server

Press `CTRL+C` in the terminal where the server is running.

## 🔧 Manual Control

If you prefer manual control:

### Start Backend Only
```bash
python3 main_simple.py
```

### Open Frontend Only
```bash
open index.html
```

## 📊 System Architecture

```
┌─────────────────┐
│   User Browser  │
│   (index.html)  │
└────────┬────────┘
         │ HTTP POST /chat
         ▼
┌─────────────────┐
│  FastAPI Server │
│ (main_simple.py)│
│                 │
│  ┌───────────┐  │
│  │  TF-IDF   │  │
│  │Vectorizer │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ Knowledge │  │
│  │   Base    │  │
│  │ (6 items) │  │
│  └───────────┘  │
└─────────────────┘
```

## 🎯 Key Features

- ✅ **100% Free** - No API keys required
- ✅ **Instant Startup** - No model downloads
- ✅ **Local Processing** - All computation on your machine
- ✅ **Image Support** - Can display images in responses
- ✅ **Confidence Scores** - Shows how confident the AI is
- ✅ **Modern UI** - Beautiful, responsive design

## 🔍 How It Works

1. **You type a question** → Frontend sends it to backend
2. **Backend vectorizes** → Converts text to numbers using TF-IDF
3. **Similarity search** → Compares against knowledge base
4. **Best match found** → Returns answer if confidence ≥ 0.40
5. **UI displays** → Shows answer with optional image

## 📝 Customization

### Add New Knowledge

Edit `main_simple.py` and add to `KNOWLEDGE_BASE`:

```python
{
    "question": "Your question here",
    "answer": "Your answer here",
    "media_url": "https://example.com/image.jpg"  # or None
}
```

Then restart the server.

### Change Confidence Threshold

In `main_simple.py`, modify:

```python
CONFIDENCE_THRESHOLD = 0.40  # Lower = more lenient
```

## 🐛 Troubleshooting

### Server won't start
- Make sure port 8000 is not in use
- Check Python version: `python3 --version` (need 3.10+)

### Frontend can't connect
- Verify server is running: `curl http://localhost:8000/health`
- Check browser console for errors (F12)

### Low confidence responses
- Try rephrasing your question
- Add more similar questions to knowledge base
- Lower the confidence threshold

## 📚 Files Overview

- `start.sh` - One-click startup script
- `main_simple.py` - Backend server (TF-IDF version)
- `main.py` - Alternative backend (sentence-transformers)
- `index.html` - Frontend chat interface
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation

## 🎉 You're All Set!

Your local AI chatbot is now running. Start asking questions and explore the capabilities!

---

**Need help?** Check the full README.md for detailed documentation.
