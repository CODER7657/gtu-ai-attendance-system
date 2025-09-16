# 🎓 GTU AI Attendance System

**An intelligent attendance management system specifically designed for Gujarat Technological University (GTU) SEM-3 CSE(DS) students**

![GTU AI Attendance System](https://img.shields.io/badge/GTU-Attendance%20System-blue)
![Next.js](https://img.shields.io/badge/Next.js-15.5.3-black)
![Node.js](https://img.shields.io/badge/Node.js-Backend-green)
![Python](https://img.shields.io/badge/Python-AI%20Service-yellow)
![Gemini AI](https://img.shields.io/badge/Gemini%20AI-1.5%20Flash-purple)

## 🚀 Features

### 🎯 GTU Policy Compliance
- **70% Minimum Attendance**: Automatic tracking for GTU exam eligibility
- **Medical Certificate Support**: 60% minimum with valid 14+ day documentation
- **Bonus Marks Calculator**: Up to 23 total bonus marks (15 + 4 + 4)
- **Real-time Warnings**: Alerts for attendance thresholds and policy violations

### 📚 SEM-3 CSE(DS) Specific
- **Subject Tracking**: DS, DBMS, PS, DF, IC, PCE with weekly class schedules
- **Division Management**: DIV-9 (Roll 1-35) and DIV-10 (Roll 36-69) support
- **Preference Learning**: AI understands liked vs disliked subjects
- **Strategic Planning**: Optimized attendance patterns based on preferences

### 🧠 AI-Powered Intelligence
- **Gemini 1.5 Flash**: Fast, accurate AI responses
- **Personalized Advice**: Context-aware recommendations
- **Document Analysis**: PDF timetable processing
- **Real-time Chat**: 24/7 AI assistant for attendance queries

### 💻 Modern Web Interface
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live attendance tracking
- **Interactive Dashboard**: Visual progress indicators
- **File Upload**: Drag-and-drop timetable processing

## 🏗️ Architecture

```
├── frontend/          # Next.js 15.5.3 React application
├── backend/           # Express.js API server  
├── ai-services/       # Python Flask + Gemini AI service
└── docs/             # Documentation and guides
```

### Components:
- **Frontend** (Port 3000): Modern React UI with TypeScript
- **Backend** (Port 5000): Express.js API with file processing
- **AI Service** (Port 5001): Python Flask with Gemini AI integration

## 🛠️ Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+ with pip
- Git
- Gemini API key (free from Google AI Studio)

### 1. Clone Repository
```bash
git clone https://github.com/CODER7657/gtu-ai-attendance-system.git
cd gtu-ai-attendance-system
```

### 2. Backend Setup
```bash
cd backend
npm install
```

### 3. Frontend Setup  
```bash
cd frontend
npm install
```

### 4. AI Service Setup
```bash
cd ai-services
pip install -r requirements.txt
```

### 5. Environment Configuration
Create `.env` files in `/backend` and `/ai-services`:

**backend/.env:**
```
PORT=5000
AI_SERVICE_URL=http://localhost:5001
NODE_ENV=development
```

**ai-services/.env:**
```
GEMINI_API_KEY=your-gemini-api-key-here
FLASK_ENV=development
```

## 🚦 Quick Start

### Start All Services:

**Terminal 1 - AI Service:**
```bash
cd ai-services
python ai_service_gemini.py
```

**Terminal 2 - Backend:**
```bash
cd backend
npm start
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application:
- **Main App**: http://localhost:3000
- **Dashboard**: http://localhost:3000/dashboard
- **Chat**: http://localhost:3000/chat  
- **Upload**: http://localhost:3000/upload

## 📊 Usage Guide

### 1. Dashboard Overview
- View current 72% attendance status
- Check GTU exam eligibility
- See bonus marks potential (15 current)
- Monitor subject-wise performance

### 2. Upload Timetable
- Drag-and-drop PDF timetable
- AI automatically extracts class schedules
- System processes division-specific timing

### 3. AI Chat Assistant
Ask questions like:
- "How many classes do I need to maintain 70%?"
- "Which subjects should I prioritize?"
- "What's my bonus marks potential?"
- "Am I safe for GTU exams?"

### 4. Strategic Planning
- **Maintain Current (72%)**: Can skip 53/190 remaining classes
- **Safe Buffer (75%)**: Can skip 40/190 remaining classes
- **Bonus Optimization (80%)**: Can skip 30/190 remaining classes

## 📈 Current Status Example

### Your GTU Profile:
- **Overall Attendance**: 72% (SAFE - above 70%)
- **Classes Completed**: 137 out of 190
- **Remaining Time**: 10 weeks in semester
- **Exam Eligible**: ✅ YES
- **Bonus Marks**: 15 available (11 attendance + 4 first-days)

### Subject Breakdown:
| Subject | Code | Attendance | Status | Weekly Classes |
|---------|------|------------|---------|----------------|
| Data Structures | DS | 85% | 💚 Liked | 4 |
| Database Systems | DBMS | 80% | 💚 Liked | 4 |
| Probability & Stats | PS | 75% | 💚 Liked | 3 |
| Digital Fundamentals | DF | 70% | 🟡 Neutral | 4 |
| Indian Constitution | IC | 55% | 🔴 Needs Attention | 2 |
| Communication Ethics | PCE | 60% | 🔴 Needs Attention | 2 |

## 🔧 API Endpoints

### Backend (Port 5000)
- `POST /api/upload` - File upload processing
- `POST /api/calculate-attendance` - Attendance calculations
- `POST /api/chat` - AI chat interface
- `POST /api/process-preferences` - User preference analysis

### AI Service (Port 5001)  
- `POST /chat` - Gemini AI chat processing
- `POST /process-document` - PDF document analysis
- `GET /health` - Service health check

## 🎯 GTU Policy Integration

### Attendance Rules:
- **Minimum Required**: 70% for exam eligibility
- **Medical Relaxation**: 60% with valid certificate (14+ consecutive days)
- **Late Policy**: >5 minutes late = marked absent
- **Proxy Penalty**: Strict punishment, bonus marks forfeited

### Bonus Marks System:
1. **Attendance Bonus**: Up to 15 marks based on percentage
2. **First 4 Days**: 4 marks if attended all classes (July 21-24, 2025)  
3. **All Clear**: 4 marks if all subjects pass after other bonuses
4. **Maximum Total**: 23 bonus marks possible

### Critical Thresholds:
- **Below 60%**: Exam ineligible (even with medical)
- **Below 70%**: Need medical certificate or lose all bonuses
- **Form Deadline**: Must maintain 70% until GTU form submission

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Gujarat Technological University** for attendance policies
- **Google Gemini AI** for intelligent processing
- **Next.js & React** for modern web framework
- **SEM-3 CSE(DS) Students** for real-world requirements

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/CODER7657/gtu-ai-attendance-system/issues)
- **Email**: your-email@example.com
- **Documentation**: Check `/docs` folder for detailed guides

---

**Made with ❤️ for GTU SEM-3 CSE(DS) Students**

*Achieve optimal attendance while maintaining academic balance!* 🎓✨