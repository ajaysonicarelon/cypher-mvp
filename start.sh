#!/bin/bash

echo "🚀 Starting Local AI Chatbot..."
echo ""
echo "📦 Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✅ Python 3 found"
echo ""
echo "🔧 Installing/updating dependencies..."
pip3 install -r requirements.txt --quiet

echo ""
echo "🤖 Starting backend server..."
echo "   API will be available at: http://localhost:8000"
echo "   Frontend will open in your browser automatically"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python3 main_simple.py &
SERVER_PID=$!

sleep 3

if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server started successfully!"
    echo ""
    echo "🌐 Opening frontend in browser..."
    open index.html
    echo ""
    echo "💬 You can now chat with your AI assistant!"
    echo ""
    
    wait $SERVER_PID
else
    echo "❌ Failed to start server"
    exit 1
fi
