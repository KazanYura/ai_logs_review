@echo off
echo 🚀 Starting AI Logs Review Development Environment
echo =================================================

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Start backend
echo 📡 Starting FastAPI backend...
start /B cmd /c "python main.py"
timeout /t 3 /nobreak >nul

REM Check if frontend exists and start it
if exist "frontend" (
    echo 🎨 Starting React frontend...
    cd frontend
    
    REM Install dependencies if node_modules doesn't exist
    if not exist "node_modules" (
        echo 📦 Installing frontend dependencies...
        npm install
    )
    
    REM Start React dev server
    start /B cmd /c "npm start"
    cd ..
    
    echo ✅ Development environment started!
    echo.
    echo 🔗 URLs:
    echo    Backend API: http://localhost:8000
    echo    Frontend UI: http://localhost:3000
    echo    API Docs: http://localhost:8000/docs
    echo.
    echo Press any key to stop all services
    pause >nul
    
    REM Kill processes (Note: this is a simplified approach)
    taskkill /f /im python.exe 2>nul
    taskkill /f /im node.exe 2>nul
) else (
    echo ⚠️  Frontend directory not found. Only backend is running.
    echo 🔗 Backend API: http://localhost:8000
    echo 🔗 API Docs: http://localhost:8000/docs
    echo.
    echo Press any key to stop backend
    pause >nul
    taskkill /f /im python.exe 2>nul
)
