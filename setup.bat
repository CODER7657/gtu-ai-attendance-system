@echo off
REM GTU AI Attendance System Setup Script for Windows

echo 🎓 Setting up GTU AI Attendance System...

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    echo    Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    echo    Download from: https://python.org/
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Setup Backend
echo 📦 Installing backend dependencies...
cd backend
if not exist ".env" (
    copy .env.example .env
    echo 📝 Created backend/.env from template - please configure your settings
)
call npm install
cd ..

REM Setup Frontend
echo 🎨 Installing frontend dependencies...
cd frontend
if not exist ".env.local" (
    copy .env.example .env.local
    echo 📝 Created frontend/.env.local from template
)
call npm install
cd ..

REM Setup AI Services
echo 🧠 Installing AI service dependencies...
cd ai-services
if not exist ".env" (
    copy .env.example .env
    echo 📝 Created ai-services/.env from template - please add your Gemini API key
)

REM Create Python virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    echo 🐍 Created Python virtual environment
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo.
echo 🎉 Setup complete!
echo.
echo 📋 Next steps:
echo 1. Add your Gemini API key to ai-services/.env
echo    Get it from: https://makersuite.google.com/app/apikey
echo.
echo 2. Start the services:
echo    Terminal 1: cd ai-services ^&^& python ai_service_gemini.py
echo    Terminal 2: cd backend ^&^& npm start
echo    Terminal 3: cd frontend ^&^& npm run dev
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
echo 📖 For detailed instructions, see README.md

pause