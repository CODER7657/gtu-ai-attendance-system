const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5001';

// Configure CORS to allow requests from frontend
app.use(cors({
    origin: 'http://localhost:3000',
    credentials: true
}));

app.use(express.json());
app.use(express.static('uploads'));

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, 'file-' + uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({ 
    storage: storage,
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB limit
    },
    fileFilter: (req, file, cb) => {
        const allowedTypes = /jpeg|jpg|png|pdf/;
        const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = allowedTypes.test(file.mimetype);
        
        if (mimetype && extname) {
            return cb(null, true);
        } else {
            cb(new Error('Only images and PDFs are allowed'));
        }
    }
});

// Create uploads directory
if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}

// Helper function to call AI service
async function callAIService(endpoint, data, isFormData = false) {
    try {
        const config = {
            method: 'POST',
            url: `${AI_SERVICE_URL}${endpoint}`,
            timeout: 30000 // 30 second timeout
        };

        if (isFormData) {
            config.data = data;
            config.headers = { 'Content-Type': 'multipart/form-data' };
        } else {
            config.data = data;
            config.headers = { 'Content-Type': 'application/json' };
        }

        const response = await axios(config);
        return response.data;
    } catch (error) {
        console.error(`AI Service Error (${endpoint}):`, error.message);
        throw new Error(`AI service unavailable: ${error.message}`);
    }
}

// Routes
app.get('/', (req, res) => {
    res.json({ 
        message: 'AI Attendance Management API - Gemini Powered',
        version: '2.0',
        features: ['gemini-ai', 'dynamic-analysis', 'web-automation', 'predictive-insights']
    });
});

// Enhanced health check that includes AI service status
app.get('/health', async (req, res) => {
    try {
        // Check AI service health
        const aiHealth = await axios.get(`${AI_SERVICE_URL}/health`, { timeout: 5000 });
        
        res.json({ 
            status: 'healthy', 
            message: 'Backend server is running',
            services: {
                backend: 'online',
                ai_service: aiHealth.data.status || 'online',
                ai_model: aiHealth.data.model || 'gemini-1.5-pro'
            },
            features: ['file_upload', 'gemini_ai', 'dynamic_analysis'],
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.json({
            status: 'partial',
            message: 'Backend running, AI service unavailable',
            services: {
                backend: 'online',
                ai_service: 'offline'
            },
            timestamp: new Date().toISOString()
        });
    }
});

// Enhanced file upload with Gemini AI processing
app.post('/api/upload', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        const { uploadType } = req.body; // 'calendar' or 'timetable'
        
        console.log(`Processing ${uploadType} file with Gemini AI:`, req.file.filename);
        
        // Prepare form data for AI service
        const FormData = require('form-data');
        const formData = new FormData();
        formData.append('file', fs.createReadStream(req.file.path));
        formData.append('type', uploadType || 'calendar');

        try {
            // Call Gemini AI service for document processing
            const aiResponse = await callAIService('/process-document', formData, true);
            
            res.json({
                success: true,
                message: `${uploadType} uploaded and processed with Gemini AI`,
                filename: req.file.filename,
                originalName: req.file.originalname,
                uploadType: uploadType,
                ai_analysis: aiResponse,
                processing_method: 'gemini-vision'
            });
        } catch (aiError) {
            // Fallback processing if AI service is unavailable
            console.warn('AI service unavailable, using fallback processing');
            res.json({
                success: true,
                message: `${uploadType} uploaded successfully (AI processing unavailable)`,
                filename: req.file.filename,
                originalName: req.file.originalname,
                uploadType: uploadType,
                processing_method: 'fallback',
                note: 'Document uploaded successfully. Enable AI service for advanced analysis.'
            });
        }
    } catch (error) {
        console.error('Upload error:', error);
        res.status(500).json({ error: 'Failed to upload file' });
    }
});

// Enhanced preferences processing with Gemini AI
app.post('/api/preferences', async (req, res) => {
    try {
        const { preferences } = req.body;
        
        if (!preferences) {
            return res.status(400).json({ error: 'No preferences provided' });
        }

        console.log('Processing preferences with Gemini AI:', preferences.substring(0, 100) + '...');

        try {
            // Call Gemini AI service for advanced preference analysis
            const aiResponse = await callAIService('/process-preferences', { preferences });
            
            res.json({
                success: true,
                message: 'Preferences analyzed with Gemini AI',
                ...aiResponse,
                enhanced_with: 'gemini-ai'
            });
        } catch (aiError) {
            // Fallback to basic keyword analysis
            const analysis = basicPreferenceAnalysis(preferences);
            res.json({
                success: true,
                message: 'Preferences processed (basic analysis)',
                analyzedPreferences: analysis,
                originalPreferences: preferences,
                processing_method: 'fallback',
                note: 'Basic analysis used. Enable AI service for advanced insights.'
            });
        }
    } catch (error) {
        console.error('Preference processing error:', error);
        res.status(500).json({ error: 'Failed to process preferences' });
    }
});

// Enhanced attendance calculation endpoint
app.post('/api/calculate-attendance', (req, res) => {
    try {
        const { 
            totalClasses, 
            attendedClasses, 
            plannedAbsences, 
            preferences,
            targetPercentage 
        } = req.body;
        
        if (!totalClasses || attendedClasses === undefined) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        // Calculate current percentage
        const currentPercentage = (attendedClasses / totalClasses) * 100;
        const target = targetPercentage || 70.5;
        
        // Calculate classes needed for target
        let classesNeeded = 0;
        if (currentPercentage < target) {
            classesNeeded = Math.ceil((target * totalClasses - 100 * attendedClasses) / (100 - target));
        }

        // Calculate safety buffer
        const safetyBuffer = currentPercentage - target;

        const analysis = {
            current_percentage: parseFloat(currentPercentage.toFixed(2)),
            target_percentage: target,
            safety_buffer: parseFloat(safetyBuffer.toFixed(2)),
            classes_needed: Math.max(0, classesNeeded),
            status: currentPercentage >= target ? 'on_track' : 'needs_improvement',
            risk_level: getRiskLevel(currentPercentage),
            recommendations: generateRecommendations(currentPercentage, target, classesNeeded, preferences),
            trend_analysis: 'stable', // Would be calculated from historical data
            next_milestone: calculateNextMilestone(currentPercentage, target)
        };

        res.json({
            success: true,
            attendance_analysis: analysis,
            calculation_method: 'enhanced',
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        console.error('Calculation error:', error);
        res.status(500).json({ error: 'Failed to calculate attendance' });
    }
});

// New endpoint: Generate AI recommendations
app.post('/api/generate-recommendations', async (req, res) => {
    try {
        const requestData = req.body;
        
        console.log('Generating AI recommendations for user data...');
        
        // Call Gemini AI service for intelligent recommendations
        const aiResponse = await callAIService('/generate-recommendations', requestData);
        
        res.json({
            success: true,
            ...aiResponse,
            enhanced_features: ['personalized', 'dynamic', 'predictive']
        });
    } catch (error) {
        // Fallback recommendations
        const fallbackRecs = generateBasicRecommendations(req.body.attendance_data || {});
        res.json({
            success: true,
            recommendations: fallbackRecs,
            processing_method: 'fallback',
            note: 'Basic recommendations provided. Enable AI service for advanced analysis.'
        });
    }
});

// New endpoint: Analyze web flow patterns
app.post('/api/analyze-web-flow', async (req, res) => {
    try {
        const webData = req.body;
        
        console.log('Analyzing web flow patterns with Gemini AI...');
        
        const aiResponse = await callAIService('/analyze-web-flow', webData);
        
        res.json({
            success: true,
            ...aiResponse,
            analysis_type: 'gemini-behavioral'
        });
    } catch (error) {
        res.json({
            success: false,
            error: 'Web flow analysis requires AI service',
            message: 'Enable Gemini AI service for behavioral analysis features'
        });
    }
});

// New endpoint: Get dynamic updates
app.get('/api/dynamic-update', async (req, res) => {
    try {
        const response = await axios.get(`${AI_SERVICE_URL}/dynamic-update`);
        res.json(response.data);
    } catch (error) {
        res.json({
            success: true,
            dynamic_update: {
                status: 'System running',
                message: 'Enable AI service for real-time insights',
                timestamp: new Date().toISOString()
            },
            note: 'Basic status provided. Connect AI service for dynamic updates.'
        });
    }
});

// New endpoint: Predict future attendance
app.post('/api/predict-attendance', async (req, res) => {
    try {
        const predictionData = req.body;
        
        console.log('Generating attendance predictions with Gemini AI...');
        
        const aiResponse = await callAIService('/predict-attendance', predictionData);
        
        res.json({
            success: true,
            ...aiResponse,
            prediction_engine: 'gemini-ai'
        });
    } catch (error) {
        res.json({
            success: false,
            error: 'Attendance prediction requires AI service',
            message: 'Enable Gemini AI for predictive analysis capabilities'
        });
    }
});

// Utility functions
function basicPreferenceAnalysis(preferences) {
    const keywords = {
        subjects: {
            liked: ['math', 'science', 'physics', 'chemistry', 'biology', 'computer', 'programming', 'engineering'],
            disliked: ['history', 'literature', 'art', 'music', 'language']
        },
        times: {
            morning: ['morning', '8am', '9am', '10am', 'early'],
            evening: ['evening', 'afternoon', '2pm', '3pm', '4pm', 'late']
        }
    };

    return {
        likedSubjects: keywords.subjects.liked.filter(subject => 
            preferences.toLowerCase().includes(subject)
        ),
        dislikedSubjects: keywords.subjects.disliked.filter(subject => 
            preferences.toLowerCase().includes(subject)
        ),
        preferredTimes: keywords.times.morning.some(time => 
            preferences.toLowerCase().includes(time)
        ) ? ['morning'] : ['evening'],
        confidence_score: 0.65,
        analysis_method: 'keyword-based'
    };
}

function getRiskLevel(percentage) {
    if (percentage >= 80) return 'low';
    if (percentage >= 75) return 'medium';
    if (percentage >= 70) return 'high';
    return 'critical';
}

function calculateNextMilestone(current, target) {
    const milestones = [60, 65, 70, 75, 80, 85, 90, 95];
    return milestones.find(milestone => milestone > current) || target;
}

function generateRecommendations(currentPercentage, target, classesNeeded, preferences) {
    const recommendations = [];
    
    if (currentPercentage >= target) {
        recommendations.push({
            type: 'achievement',
            message: '🎉 Excellent! You\'re exceeding your attendance target.',
            priority: 'low'
        });
        recommendations.push({
            type: 'maintenance',
            message: '💪 Maintain this consistency to stay ahead.',
            priority: 'medium'
        });
    } else {
        recommendations.push({
            type: 'action_required',
            message: `📊 Attend ${classesNeeded} more classes to reach ${target}% attendance.`,
            priority: 'high'
        });
        recommendations.push({
            type: 'strategy',
            message: '⏰ Set daily reminders 30 minutes before each class.',
            priority: 'medium'
        });
    }
    
    if (currentPercentage < 65) {
        recommendations.push({
            type: 'critical',
            message: '🚨 CRITICAL: Immediate action required to avoid academic consequences.',
            priority: 'critical'
        });
    } else if (currentPercentage < 70) {
        recommendations.push({
            type: 'warning',
            message: '⚠️ WARNING: Below minimum requirement. Prioritize attendance now.',
            priority: 'high'
        });
    }
    
    return recommendations;
}

function generateBasicRecommendations(attendanceData) {
    return {
        immediate_actions: [
            'Review current attendance status',
            'Plan next week\'s class schedule',
            'Set up attendance reminders'
        ],
        long_term_strategy: [
            'Maintain consistent attendance pattern',
            'Monitor weekly progress',
            'Adjust schedule as needed'
        ],
        note: 'Enable AI service for personalized, intelligent recommendations'
    };
}

// New endpoint: AI Chat Assistant
app.post('/api/chat', async (req, res) => {
    try {
        const { message, context } = req.body;
        
        if (!message || message.trim() === '') {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log('🤖 Processing AI chat message:', message);
        
        // GTU-specific student data (your actual situation)
        const gtuStudentData = {
            current_attendance: 72.0,
            total_classes_completed: 190,
            attended_classes: 137,
            remaining_weeks: 10,
            exam_eligible: true,
            bonus_eligible: true,
            
            subjects: {
                DS: { name: "Data Structures", attendance: 85, weekly_classes: 4, type: "liked" },
                DBMS: { name: "Database Management System", attendance: 80, weekly_classes: 4, type: "liked" },
                PS: { name: "Probability and Statistics", attendance: 75, weekly_classes: 3, type: "liked" },
                DF: { name: "Digital Fundamentals", attendance: 70, weekly_classes: 4, type: "neutral" },
                IC: { name: "Indian Constitution", attendance: 55, weekly_classes: 2, type: "disliked" },
                PCE: { name: "Professional Communication and Ethics", attendance: 60, weekly_classes: 2, type: "disliked" }
            },
            
            bonus_marks: {
                attendance: 11, // (72/100) * 15 ≈ 11
                first_four_days: 4,
                all_clear: 0,
                total: 15
            },
            
            gtu_policies: {
                minimum_exam_eligibility: 70,
                minimum_with_medical: 60,
                max_attendance_bonus: 15,
                first_four_days_bonus: 4,
                all_clear_bonus: 4
            },
            
            scenarios: {
                maintain_current: { required_to_attend: 137, remaining_classes: 190, can_skip: 53, final_attendance: 72.0 },
                safe_buffer: { required_to_attend: 150, remaining_classes: 190, can_skip: 40, final_attendance: 75.0 },
                bonus_optimization: { required_to_attend: 160, remaining_classes: 190, can_skip: 30, final_attendance: 80.0 },
                minimum_safe: { required_to_attend: 134, remaining_classes: 190, can_skip: 56, final_attendance: 70.1 }
            },
            
            warnings: [
                "✅ SAFE: Currently eligible for exams and bonus marks",
                "⚠️ CAUTION: Close to danger zone - Monitor carefully and maintain buffer",
                "⚠️ SUBJECTS: IC (55%) and PCE (60%) below ideal levels - consider strategic attendance"
            ]
        };
        
        // Enhanced context with real GTU data
        const enhancedContext = {
            ...context,
            student_data: gtuStudentData,
            university: "GTU",
            semester: "SEM-3",
            program: "CSE(DS)",
            current_date: new Date().toISOString(),
            academic_year: "2025"
        };
        
        // Call Gemini AI service with comprehensive GTU context
        const chatData = {
            message: message.trim(),
            context: enhancedContext,
            timestamp: new Date().toISOString()
        };
        
        const aiResponse = await callAIService('/chat', chatData);
        
        res.json({
            success: true,
            response: aiResponse.response,
            context_used: aiResponse.context_used || true,
            suggestions: aiResponse.suggestions || [
                "How many classes do I need to attend to maintain 70%?",
                "What's my bonus marks potential with current attendance?", 
                "Which subjects should I focus on attending?",
                "Am I safe for GTU exam eligibility?",
                "How can I optimize my attendance strategy?"
            ],
            student_data: gtuStudentData, // Include data for frontend reference
            timestamp: new Date().toISOString(),
            processing_method: 'gemini-ai-gtu'
        });
        
    } catch (error) {
        console.error('Chat error:', error);
        
        // Enhanced fallback response with GTU context
        const fallbackResponse = {
            success: true,
            response: `Based on your current 72% attendance status, you are eligible for GTU exams and bonus marks. With 10 weeks remaining in SEM-3, you need to maintain attendance above 70%. Your liked subjects (DS, DBMS, PS) are performing well, but IC (55%) and PCE (60%) need attention. You can earn up to 15 attendance bonus marks currently.`,
            context_used: false,
            suggestions: [
                "How many more classes do I need to attend?",
                "What's my current bonus marks eligibility?",
                "Should I focus on IC and PCE attendance?",
                "What happens if I drop below 70%?"
            ],
            processing_method: 'fallback-gtu',
            note: 'AI service temporarily unavailable - using GTU data fallback'
        };
        
        res.json(fallbackResponse);
    }
});

app.listen(PORT, () => {
    console.log(`🚀 AI Attendance Backend Server running on port ${PORT}`);
    console.log(`🧠 AI Service URL: ${AI_SERVICE_URL}`);
    console.log(`✨ Features: Gemini AI, Dynamic Analysis, Predictive Insights`);
});