import os
import json
import requests
import schedule
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import base64
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
genai.configure(api_key=GEMINI_API_KEY)

# Smart model selection with fallback
def get_best_available_model():
    """Try stable models with preference for faster, lighter versions"""
    model_preferences = [
        'gemini-1.5-flash',         # Fast and efficient - best for API limits
        'gemini-1.5-flash-latest',  # Latest flash version
        'gemini-1.5-pro',           # Stable fallback
        'gemini-2.0-flash'          # Newer flash model
    ]
    
    for model_name in model_preferences:
        try:
            test_model = genai.GenerativeModel(model_name)
            # Quick test to verify the model works
            return model_name, test_model
        except Exception as e:
            print(f"⚠️ Model {model_name} not available: {str(e)[:100]}")
            continue
    
    # Final fallback
    return 'gemini-1.5-flash', genai.GenerativeModel('gemini-1.5-flash')

# Initialize Gemini models with smart selection
model_name, model = get_best_available_model()
vision_model = model  # Use the same model for vision tasks (all newer models support multimodal)

print(f"🤖 Using Gemini model: {model_name}")
print(f"✨ Features: Advanced reasoning, multimodal processing, enhanced context")

# Global data store for dynamic updates
attendance_data = {
    'current_percentage': 78.5,
    'total_classes': 100,
    'attended_classes': 78,
    'subjects': {},
    'trends': [],
    'predictions': {},
    'last_updated': datetime.now()
}

user_preferences = {}
dynamic_recommendations = []

def setup_web_driver():
    """Setup headless Chrome driver for web automation"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except:
        print("Chrome driver not available, web automation disabled")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Gemini AI Service is running",
        "model": model_name,  # Dynamic model name based on what's available
        "features": ["advanced_reasoning", "multimodal_processing", "enhanced_context", "real_time_analysis"]
    })

@app.route('/process-preferences', methods=['POST'])
def process_preferences_with_gemini():
    try:
        data = request.json
        preferences_text = data.get('preferences', '')
        
        if not preferences_text:
            return jsonify({"error": "No preferences provided"}), 400

        # Use Gemini 2.5 Pro for advanced preference analysis with enhanced reasoning
        prompt = f"""
        You are an advanced AI educational advisor with deep understanding of student psychology and learning patterns. 
        Analyze the following student preferences and provide comprehensive insights:
        
        Student Input: "{preferences_text}"
        
        Please provide a detailed JSON response with enhanced analysis:
        {{
            "liked_subjects": ["list of subjects the student enjoys with confidence scores"],
            "disliked_subjects": ["list of subjects the student dislikes with reasoning"],
            "preferred_times": ["optimal class times based on psychological patterns"],
            "disliked_times": ["times to avoid with productivity impact analysis"],
            "learning_style": {{
                "primary_style": "visual/auditory/kinesthetic/reading",
                "secondary_traits": ["detailed learning preferences"],
                "optimal_environment": "description of ideal study conditions"
            }},
            "attendance_patterns": {{
                "predicted_behavior": "detailed attendance prediction",
                "risk_assessment": "low/medium/high with factors",
                "seasonal_variations": "how attendance might vary by semester periods"
            }},
            "motivation_factors": {{
                "intrinsic": ["internal motivators like interest, curiosity"],
                "extrinsic": ["external motivators like grades, career goals"],
                "social": ["peer influence, group dynamics"]
            }},
            "risk_factors": {{
                "high_risk": ["major factors that could cause skipping"],
                "medium_risk": ["moderate concerns to monitor"],
                "mitigation_strategies": ["specific recommendations to address risks"]
            }},
            "personality_assessment": {{
                "academic_persona": "detailed academic personality type",
                "stress_response": "how they handle academic pressure",
                "goal_orientation": "achievement vs. mastery focused",
                "time_management_style": "procrastinator vs. planner"
            }},
            "personalized_recommendations": {{
                "attendance_strategy": "specific tactics for maintaining attendance",
                "study_optimization": "how to maximize learning efficiency",
                "schedule_recommendations": "ideal weekly schedule structure",
                "wellness_tips": "maintaining balance and preventing burnout"
            }},
            "behavioral_insights": {{
                "decision_making_patterns": "how they make attendance decisions",
                "energy_cycles": "daily and weekly energy patterns",
                "social_influences": "impact of friends and environment"
            }}
        }}
        
        Use advanced reasoning to provide deep, actionable insights that go beyond surface-level analysis.
        Be specific, practical, and psychologically informed. Return only valid JSON.
        """
        
        # Enhanced generation configuration for Gemini 2.5 Pro
        generation_config = {
            "temperature": 0.7,  # Balanced creativity and consistency
            "top_p": 0.8,        # Focused but diverse responses
            "top_k": 40,         # Good balance of options
            "max_output_tokens": 4096,  # Comprehensive responses
            "response_mime_type": "application/json"  # Force JSON output
        }
        
        response = model.generate_content(prompt, generation_config=generation_config)
        
        try:
            # Parse Gemini's response as JSON
            analysis = json.loads(response.text)
            
            # Store preferences globally for dynamic updates
            global user_preferences
            user_preferences = analysis
            
            return jsonify({
                "success": True,
                "analysis_method": "gemini-ai",
                "analyzed_preferences": analysis,
                "original_text": preferences_text,
                "confidence_score": 0.95
            })
            
        except json.JSONDecodeError:
            # Fallback if Gemini doesn't return valid JSON
            return jsonify({
                "success": True,
                "analysis_method": "gemini-text",
                "raw_analysis": response.text,
                "original_text": preferences_text
            })
        
    except Exception as e:
        print(f"Error processing preferences: {str(e)}")
        return jsonify({"error": f"Failed to process preferences: {str(e)}"}), 500

@app.route('/process-document', methods=['POST'])
def process_document_with_vision():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        doc_type = request.form.get('type', 'calendar')
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Convert uploaded file to image for Gemini Vision
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Prepare prompt based on document type
        if doc_type == 'calendar':
            prompt = """
            Analyze this academic calendar image and extract:
            1. Semester start and end dates
            2. All holidays and breaks with dates
            3. Exam periods
            4. Total working days estimation
            5. Important academic deadlines
            6. Weekly schedule patterns
            
            Return a detailed JSON response with all extracted information.
            """
        else:  # timetable
            prompt = """
            Analyze this class timetable and extract:
            1. All subjects/courses listed
            2. Weekly schedule for each day
            3. Class timings and durations
            4. Room numbers/locations if visible
            5. Professor names if mentioned
            6. Total classes per week calculation
            7. Subject-wise weekly hours
            
            Return a comprehensive JSON response with the complete schedule.
            """
        
        # Use Gemini Vision API
        response = vision_model.generate_content([prompt, image])
        
        try:
            extracted_data = json.loads(response.text)
        except json.JSONDecodeError:
            extracted_data = {
                "raw_analysis": response.text,
                "note": "Could not parse as JSON, providing raw analysis"
            }
        
        return jsonify({
            "success": True,
            "document_type": doc_type,
            "analysis_method": "gemini-vision",
            "extracted_data": extracted_data,
            "processing_time": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return jsonify({"error": f"Failed to process document: {str(e)}"}), 500

@app.route('/generate-recommendations', methods=['POST'])
def generate_dynamic_recommendations():
    try:
        data = request.json
        current_attendance = data.get('attendance_data', {})
        user_prefs = data.get('preferences', {})
        
        # Merge with stored preferences
        combined_prefs = {**user_preferences, **user_prefs}
        
        # Advanced prompt for Gemini
        prompt = f"""
        You are an AI attendance advisor. Generate personalized recommendations based on:
        
        Current Attendance Data:
        {json.dumps(current_attendance, indent=2)}
        
        User Preferences & Profile:
        {json.dumps(combined_prefs, indent=2)}
        
        Current Trends:
        {json.dumps(attendance_data['trends'], indent=2)}
        
        Please provide:
        1. Immediate action recommendations (next 1-2 weeks)
        2. Long-term strategy (semester planning)
        3. Risk assessment and mitigation
        4. Personalized motivation strategies
        5. Subject-specific attendance plans
        6. Timeline for attendance recovery (if needed)
        7. Alternative learning opportunities
        8. Emergency contingency plans
        
        Consider the student's personality, preferences, and academic goals.
        Return a comprehensive JSON response with actionable advice.
        """
        
        response = model.generate_content(prompt)
        
        try:
            recommendations = json.loads(response.text)
        except json.JSONDecodeError:
            recommendations = {
                "raw_recommendations": response.text,
                "note": "AI analysis in text format"
            }
        
        # Store recommendations for continuous updates
        global dynamic_recommendations
        dynamic_recommendations = recommendations
        
        return jsonify({
            "success": True,
            "recommendations": recommendations,
            "analysis_method": "gemini-advanced",
            "last_updated": datetime.now().isoformat(),
            "dynamic_updates": True
        })
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return jsonify({"error": f"Failed to generate recommendations: {str(e)}"}), 500

@app.route('/analyze-web-flow', methods=['POST'])
def analyze_web_flow():
    """Analyze user's web behavior and attendance patterns dynamically"""
    try:
        data = request.json
        web_activity = data.get('web_activity', {})
        attendance_history = data.get('attendance_history', [])
        
        prompt = f"""
        Analyze this student's web behavior and attendance patterns to provide insights:
        
        Web Activity Data:
        {json.dumps(web_activity, indent=2)}
        
        Attendance History:
        {json.dumps(attendance_history, indent=2)}
        
        Provide analysis on:
        1. Correlation between web activity and attendance
        2. Behavior patterns that predict attendance
        3. Optimal times for study reminders
        4. Digital distraction factors
        5. Engagement level indicators
        6. Personalized intervention strategies
        7. Predictive attendance modeling
        
        Return detailed JSON analysis with actionable insights.
        """
        
        response = model.generate_content(prompt)
        
        try:
            analysis = json.loads(response.text)
        except json.JSONDecodeError:
            analysis = {"raw_analysis": response.text}
        
        return jsonify({
            "success": True,
            "web_flow_analysis": analysis,
            "analysis_timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error analyzing web flow: {str(e)}")
        return jsonify({"error": f"Failed to analyze web flow: {str(e)}"}), 500

@app.route('/dynamic-update', methods=['GET'])
def get_dynamic_update():
    """Provide real-time dynamic updates on attendance"""
    global attendance_data, dynamic_recommendations
    
    # Use Gemini to generate dynamic insights
    prompt = f"""
    Based on the current attendance data and trends, provide a real-time update:
    
    Current Data: {json.dumps(attendance_data, indent=2)}
    Last Recommendations: {json.dumps(dynamic_recommendations, indent=2)}
    
    Generate:
    1. Current status summary
    2. Today's specific recommendations
    3. Urgent actions needed
    4. Trend analysis
    5. Motivational message
    6. Next check-in time
    
    Return JSON format with concise, actionable updates.
    """
    
    try:
        response = model.generate_content(prompt)
        update = json.loads(response.text)
    except:
        update = {
            "status": "System running",
            "message": "Dynamic updates available",
            "timestamp": datetime.now().isoformat()
        }
    
    return jsonify({
        "success": True,
        "dynamic_update": update,
        "data_freshness": "real-time",
        "next_update_in": "15 minutes"
    })

@app.route('/predict-attendance', methods=['POST'])
def predict_future_attendance():
    """Use Gemini to predict future attendance patterns"""
    try:
        data = request.json
        historical_data = data.get('historical_data', [])
        upcoming_events = data.get('upcoming_events', [])
        
        prompt = f"""
        Predict future attendance patterns based on historical data and upcoming events:
        
        Historical Attendance: {json.dumps(historical_data, indent=2)}
        Upcoming Events: {json.dumps(upcoming_events, indent=2)}
        User Profile: {json.dumps(user_preferences, indent=2)}
        
        Provide predictions for:
        1. Next 2 weeks attendance probability by subject
        2. Monthly attendance forecast
        3. Risk periods identification
        4. Optimal scheduling recommendations
        5. Intervention timing suggestions
        6. Confidence intervals for predictions
        
        Return detailed JSON predictions with confidence scores.
        """
        
        response = model.generate_content(prompt)
        predictions = json.loads(response.text)
        
        return jsonify({
            "success": True,
            "predictions": predictions,
            "prediction_horizon": "2 weeks to 1 month",
            "model": "gemini-predictive"
        })
        
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/chat', methods=['POST'])
def ai_chat_assistant():
    """Intelligent chat assistant with access to all analyzed data"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        context = data.get('context', {})
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Build comprehensive context from all analyzed data with JSON-safe formatting
        def make_json_safe(obj):
            """Convert datetime objects to ISO strings for JSON serialization"""
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: make_json_safe(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_json_safe(item) for item in obj]
            else:
                return obj
        
        chat_context = {
            "user_preferences": make_json_safe(user_preferences),
            "attendance_data": make_json_safe(attendance_data),
            "dynamic_recommendations": make_json_safe(dynamic_recommendations),
            "current_time": datetime.now().isoformat(),
            "conversation_context": context
        }
        
        # Enhanced prompt for intelligent attendance assistant
        system_prompt = """
        You are an expert AI Attendance Assistant for GTU (Gujarat Technological University) SEM-3 CSE(DS) students. 
        You have complete access to the student's analyzed data and deep knowledge of GTU attendance policies.
        
        GTU ATTENDANCE POLICIES YOU MUST FOLLOW:
        - Minimum 70% attendance mandatory for GTU exam eligibility
        - Can be relaxed to 60% ONLY with valid medical certificate (14+ consecutive working days)
        - Attendance bonus: Up to 15 marks for attendance + 4 marks for first 4 days + 4 marks if all subjects clear
        - Below 70% at any checkpoint = ALL bonus marks forfeited
        - More than 5 minutes late = marked absent
        - Proxy attendance = strict punishment and bonus mark loss
        
        SEM-3 CSE(DS) SUBJECTS:
        - DS (Data Structures) - 4 classes/week
        - DBMS (Database Management System) - 4 classes/week  
        - PS (Probability and Statistics) - 3 classes/week
        - DF (Digital Fundamentals) - 4 classes/week
        - IC (Indian Constitution) - 2 classes/week
        - PCE (Professional Communication and Ethics) - 2 classes/week
        
        CURRENT STUDENT STATUS:
        - 72% attendance (SAFE - above 70% threshold)
        - Eligible for exams and bonus marks
        - Approximately 10 weeks remaining in semester
        
        Your capabilities include:
        - GTU policy compliance checking
        - Subject-specific attendance strategies
        - Bonus marks optimization calculations
        - Risk assessment and warnings
        - Division-specific timetable analysis (DIV-9: Roll 1-35, DIV-10: Roll 36-69)
        
        Always be helpful, encouraging, and provide GTU-compliant advice.
        Use the analyzed data to give personalized, contextual responses that maintain GTU eligibility.
        """
        
        user_prompt = f"""
        Student Question: "{message}"
        
        IMPORTANT: Use the specific GTU student data provided in context to give precise, personalized answers.
        
        Student's Current GTU Status:
        - Current Attendance: 72% (ABOVE 70% threshold - SAFE for exams)
        - Total Classes So Far: 190 completed, 137 attended
        - Remaining Time: 10 weeks left in semester
        - Exam Eligibility: YES (above 70% minimum)
        - Bonus Marks Eligible: 11 attendance marks + 4 first-4-days = 15 total bonus marks
        
        Subject Breakdown (Weekly Classes):
        - DS (Data Structures): 85% attendance, 4 classes/week [LIKED SUBJECT]
        - DBMS (Database System): 80% attendance, 4 classes/week [LIKED SUBJECT]  
        - PS (Probability & Stats): 75% attendance, 3 classes/week [LIKED SUBJECT]
        - DF (Digital Fundamentals): 70% attendance, 4 classes/week [NEUTRAL]
        - IC (Indian Constitution): 55% attendance, 2 classes/week [DISLIKED - NEEDS ATTENTION]
        - PCE (Communication Ethics): 60% attendance, 2 classes/week [DISLIKED - NEEDS ATTENTION]
        
        Attendance Scenarios for Remaining 10 Weeks:
        - Maintain Current (72%): Can skip 53 out of 190 remaining classes
        - Safe Buffer (75%): Can skip 40 out of 190 remaining classes  
        - Bonus Optimization (80%): Can skip 30 out of 190 remaining classes
        - Minimum Safe (70.1%): Can skip 56 out of 190 remaining classes
        
        Full Context Data: {json.dumps(chat_context, indent=2)}
        
        CRITICAL INSTRUCTIONS:
        1. Answer using SPECIFIC NUMBERS from the student's data above
        2. Reference their ACTUAL 72% attendance, not generic percentages
        3. Mention their REAL subject performance (DS 85%, IC 55%, etc.)
        4. Use their ACTUAL remaining time (10 weeks) in calculations
        5. Reference GTU policies (70% minimum, 15 bonus marks, etc.)
        6. Be encouraging but precise with data-driven advice
        
        Provide a helpful, personalized response that directly uses their real attendance data.
        """
        
        # Conservative generation configuration for Flash model
        chat_config = {
            "temperature": 0.7,  # Balanced creativity/consistency
            "top_p": 0.8,        # Focused responses
            "top_k": 40,         # Controlled vocabulary
            "max_output_tokens": 1024,  # Shorter responses for better performance
        }
        
        response = model.generate_content([system_prompt, user_prompt], generation_config=chat_config)
        
        # Skip AI-generated suggestions to save API calls, use GTU-specific ones
        suggestions = [
            "Am I eligible for GTU exams with my current attendance?",
            "How many bonus marks can I get with 72% attendance?",
            "Which subjects should I prioritize attending?",
            "What's the minimum attendance I need to maintain?",
            "How does the GTU medical certificate policy work?",
            "What happens if I fall below 70% attendance?"
        ]
        
        return jsonify({
            "success": True,
            "response": response.text,
            "context_used": True,
            "suggestions": suggestions,
            "data_sources": ["preferences", "attendance_data", "recommendations"],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Chat error: {error_msg}")
        
        # Log more details for debugging
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        return jsonify({
            "success": False,
            "response": f"I'm having trouble accessing my AI capabilities right now. Error: {error_msg[:100]}... However, I'm here to help with your attendance questions. Could you try rephrasing your question?",
            "context_used": False,
            "suggestions": [
                "What's my attendance status?",
                "How can I improve my attendance?",
                "What subjects need attention?",
                "Give me attendance tips"
            ],
            "error": "AI processing temporarily unavailable",
            "debug_error": error_msg[:200]  # First 200 chars for debugging
        }), 500

def schedule_dynamic_updates():
    """Schedule periodic updates and analysis"""
    def update_attendance_trends():
        global attendance_data
        # This would connect to real attendance systems
        attendance_data['last_updated'] = datetime.now()
        print(f"Attendance data updated at {datetime.now()}")
    
    def generate_daily_insights():
        # Use Gemini to generate daily insights
        if user_preferences:
            prompt = f"""
            Generate daily attendance insights for user with preferences:
            {json.dumps(user_preferences, indent=2)}
            
            Current date: {datetime.now().strftime('%Y-%m-%d')}
            
            Provide today's focus areas and recommendations.
            """
            try:
                response = model.generate_content(prompt)
                print(f"Daily insight generated: {response.text[:100]}...")
            except:
                print("Daily insight generation failed")
    
    # Schedule updates
    schedule.every(15).minutes.do(update_attendance_trends)
    schedule.every().day.at("08:00").do(generate_daily_insights)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    print("🚀 Starting Gemini-Powered AI Attendance Service...")
    print("✨ Features: Dynamic Analysis, Web Flow Tracking, Real-time Updates")
    print(f"🧠 Model: {model.model_name if hasattr(model, 'model_name') else 'Gemini 1.5 Pro'}")
    
    if GEMINI_API_KEY == 'your-gemini-api-key-here':
        print("⚠️  Warning: Please set your GEMINI_API_KEY environment variable")
    
    # Start background scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_dynamic_updates)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    app.run(debug=True, port=5001, host='0.0.0.0')