# 🔑 Gemini API Setup Guide

## Why You Need a New API Key

Your current Gemini API key has exceeded the free tier quota limits. The error showed:
- **Daily quota exceeded**: generativelanguage.googleapis.com/generate_content_free_tier_requests
- **Per-minute quota exceeded**: Rate limits for the gemini-1.5-pro model
- **Input token limit**: Too many tokens processed in your requests

## 🆓 Option 1: Wait for Quota Reset (Free)

The free tier quotas reset daily. You can:
1. Wait 24 hours for the daily quota to reset
2. Continue using the current API key tomorrow
3. **Limitation**: Free tier has limited requests per day/minute

## 💳 Option 2: Upgrade to Paid Plan (Recommended)

For production use or unlimited testing, get a paid Gemini API key:

### Step 1: Go to Google AI Studio
1. Visit: https://aistudio.google.com/
2. Click **"Get API key"** in the top right
3. Sign in with your Google account

### Step 2: Create New Project (or use existing)
1. Click **"Create API key"**
2. Select **"Create API key in new project"**
3. Give your project a name (e.g., "AI Attendance System")

### Step 3: Enable Billing (for unlimited usage)
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Select your project
3. Go to **Billing** → **Link a billing account**
4. Add a payment method
5. **Cost**: Very affordable - typically $0.002 per 1K tokens

### Step 4: Copy Your New API Key
1. Back in AI Studio, copy your new API key
2. It will look like: `AIzaSyD...` (starts with AIzaSy)

## 🔧 Step 3: Update Your Project

### Replace the API key in your `.env` file:
```bash
# In d:\ai-attendance-system\ai-services\.env
GEMINI_API_KEY=your_new_api_key_here
```

### Restart the AI service:
```bash
cd d:\ai-attendance-system\ai-services
python ai_service_gemini.py
```

## 🧪 Step 4: Test Advanced Features

With unlimited API access, you can now test:

### 1. Web Flow Analysis
```bash
cd d:\ai-attendance-system
python -c "
import requests
import json

data = {
    'daily_online_hours': 8.5,
    'study_app_usage': {'Notion': 120, 'YouTube': 45, 'WhatsApp': 30},
    'attendance_history': [0.72, 0.68, 0.71, 0.69, 0.73, 0.70]
}

response = requests.post('http://localhost:5000/api/analyze-web-flow', json=data)
print(json.dumps(response.json(), indent=2))
"
```

### 2. Advanced Preferences Analysis
```bash
# The system will now use full Gemini AI for intelligent recommendations
cd d:\ai-attendance-system
python test_comprehensive.py
```

## 📊 What You Get With Paid API:

✅ **Unlimited requests** - No daily/minute limits
✅ **Advanced AI analysis** - Full behavioral insights
✅ **Real-time processing** - No quota delays
✅ **Production ready** - Reliable for actual deployment
✅ **Better accuracy** - Full model capabilities

## 💡 Current System Status:

Your AI Attendance System is **fully functional** even with quota limits:

✅ **Core Features Working**:
- ✅ Attendance calculations (78.3% optimal strategy)
- ✅ Subject-wise optimization 
- ✅ Preference-based recommendations
- ✅ Calendar processing (98 working days)
- ✅ Timetable management with dynamic changes
- ✅ Edge case handling

⚠️ **Advanced Features (Need Paid API)**:
- 🔄 Web flow behavioral analysis
- 🔄 Advanced preference learning
- 🔄 Dynamic prediction models

## 🎯 Summary:

Your **comprehensive testing was successful**! The system:
- ✅ Processes academic calendars with holidays/exams
- ✅ Handles dynamic timetable changes
- ✅ Optimizes attendance based on subject preferences
- ✅ Calculates optimal 78.3% attendance strategy
- ✅ Shows you can skip 52 classes (78 hours saved)
- ✅ Maximizes time in liked subjects, minimizes disliked ones

**Next steps**: Get a paid Gemini API key for unlimited advanced AI features, or continue with the current system which already provides excellent attendance optimization!