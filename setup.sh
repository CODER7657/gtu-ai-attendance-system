#!/bin/bash

# GTU AI Attendance System Setup Script
echo "🎓 Setting up GTU AI Attendance System..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.9+ first."
    echo "   Download from: https://python.org/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo "📦 Installing backend dependencies..."
cd backend
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Created backend/.env from template - please configure your settings"
fi
npm install
cd ..

# Setup Frontend
echo "🎨 Installing frontend dependencies..."
cd frontend
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
    echo "📝 Created frontend/.env.local from template"
fi
npm install
cd ..

# Setup AI Services
echo "🧠 Installing AI service dependencies..."
cd ai-services
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Created ai-services/.env from template - please add your Gemini API key"
fi

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "🐍 Created Python virtual environment"
fi

# Activate virtual environment and install dependencies
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

pip install -r requirements.txt
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add your Gemini API key to ai-services/.env"
echo "   Get it from: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Start the services:"
echo "   Terminal 1: cd ai-services && python ai_service_gemini.py"
echo "   Terminal 2: cd backend && npm start"
echo "   Terminal 3: cd frontend && npm run dev"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "📖 For detailed instructions, see README.md"