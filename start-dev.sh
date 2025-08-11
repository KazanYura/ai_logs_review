#!/bin/bash

# Development setup script for AI Logs Review

echo "🚀 Starting AI Logs Review Development Environment"
echo "================================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Start backend in background
echo "📡 Starting FastAPI backend..."
if command -v poetry &> /dev/null; then
    poetry install
    poetry run python main.py &
    BACKEND_PID=$!
else
    echo "⚠️  Poetry not found. Please install dependencies manually and run: python main.py"
    python main.py &
    BACKEND_PID=$!
fi

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if frontend exists and start it
if [ -d "frontend" ]; then
    echo "🎨 Starting React frontend..."
    cd frontend
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    
    # Start React dev server
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Development environment started!"
    echo ""
    echo "🔗 URLs:"
    echo "   Backend API: http://localhost:8000"
    echo "   Frontend UI: http://localhost:3000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    # Wait for user to stop
    trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT
    wait
else
    echo "⚠️  Frontend directory not found. Only backend is running."
    echo "🔗 Backend API: http://localhost:8000"
    echo "🔗 API Docs: http://localhost:8000/docs"
    
    trap "echo '🛑 Stopping backend...'; kill $BACKEND_PID 2>/dev/null; exit" SIGINT
    wait
fi
