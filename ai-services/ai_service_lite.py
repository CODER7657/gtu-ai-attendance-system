import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Note: Heavy ML models disabled for faster startup
# sentiment_analyzer = pipeline(
#     "sentiment-analysis",
#     model="cardiffnlp/twitter-roberta-base-sentiment-latest"
# )

# text_classifier = pipeline(
#     "zero-shot-classification",
#     model="facebook/bart-large-mnli"
# )

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "AI service is running"})

@app.route('/process-preferences', methods=['POST'])
def process_preferences():
    try:
        data = request.json
        preferences_text = data.get('preferences', '')
        
        if not preferences_text:
            return jsonify({"error": "No preferences provided"}), 400
        
        # Simplified preference analysis without ML models
        analyzed_preferences = {
            'liked_subjects': [],
            'disliked_subjects': [],
            'liked_times': [],
            'disliked_times': [],
            'general_sentiment': 'neutral'
        }
        
        # Simple keyword-based analysis
        preferences_lower = preferences_text.lower()
        
        # Subject detection
        subject_keywords = {
            'mathematics': ['math', 'mathematics', 'calculus', 'algebra'],
            'physics': ['physics', 'mechanics', 'thermodynamics'],
            'chemistry': ['chemistry', 'organic', 'inorganic'],
            'biology': ['biology', 'botany', 'zoology'],
            'computer science': ['computer', 'programming', 'coding', 'software'],
            'english': ['english', 'literature', 'grammar'],
            'history': ['history', 'ancient', 'modern']
        }
        
        # Time detection
        time_keywords = {
            'morning': ['morning', '8 am', '9 am', '10 am'],
            'afternoon': ['afternoon', '12 pm', '1 pm', '2 pm'],
            'evening': ['evening', '4 pm', '5 pm', '6 pm'],
            'early_morning': ['early morning', '7 am', '6 am']
        }
        
        # Positive/negative sentiment words
        positive_words = ['love', 'like', 'enjoy', 'prefer', 'favorite', 'best', 'good', 'great', 'excellent']
        negative_words = ['hate', 'dislike', 'boring', 'worst', 'bad', 'terrible', 'awful', 'avoid']
        
        sentences = preferences_text.split('.')
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if not sentence_lower:
                continue
                
            # Determine sentiment
            has_positive = any(word in sentence_lower for word in positive_words)
            has_negative = any(word in sentence_lower for word in negative_words)
            
            # Check subjects
            for subject, keywords in subject_keywords.items():
                if any(keyword in sentence_lower for keyword in keywords):
                    if has_positive and not has_negative:
                        if subject not in analyzed_preferences['liked_subjects']:
                            analyzed_preferences['liked_subjects'].append(subject)
                    elif has_negative and not has_positive:
                        if subject not in analyzed_preferences['disliked_subjects']:
                            analyzed_preferences['disliked_subjects'].append(subject)
            
            # Check times
            for time_period, keywords in time_keywords.items():
                if any(keyword in sentence_lower for keyword in keywords):
                    if has_positive and not has_negative:
                        if time_period not in analyzed_preferences['liked_times']:
                            analyzed_preferences['liked_times'].append(time_period)
                    elif has_negative and not has_positive:
                        if time_period not in analyzed_preferences['disliked_times']:
                            analyzed_preferences['disliked_times'].append(time_period)
        
        return jsonify({
            "success": True,
            "analyzed_preferences": analyzed_preferences,
            "original_text": preferences_text
        })
        
    except Exception as e:
        print(f"Error processing preferences: {str(e)}")
        return jsonify({"error": f"Failed to process preferences: {str(e)}"}), 500

@app.route('/process-document', methods=['POST'])
def process_document():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        doc_type = request.form.get('type', 'calendar')  # 'calendar' or 'timetable'
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        file.save(temp_path)
        
        try:
            if doc_type == 'calendar':
                result = process_calendar_document(temp_path)
            else:
                result = process_timetable_document(temp_path)
            
            return jsonify({
                "success": True,
                "document_type": doc_type,
                "extracted_data": result
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return jsonify({"error": f"Failed to process document: {str(e)}"}), 500

def process_calendar_document(file_path):
    """Extract calendar information from PDF/image"""
    try:
        # Simplified processing - in real version would use OCR
        calendar_data = {
            'semester_start': '2025-01-15',
            'semester_end': '2025-06-30',
            'holidays': ['Spring Break: March 15-22', 'Easter Holiday: April 18-21'],
            'total_working_days': 120,
            'exam_dates': ['Final Exams: June 15-25']
        }
        
        return calendar_data
        
    except Exception as e:
        print(f"Error processing calendar: {str(e)}")
        raise

def process_timetable_document(file_path):
    """Extract timetable information from PDF/image"""
    try:
        # Simplified processing - in real version would use OCR
        timetable_data = {
            'subjects': ['Mathematics', 'Physics', 'Chemistry', 'Computer Science'],
            'weekly_schedule': {
                'monday': [
                    {'subject': 'Mathematics', 'time': '9:00 AM', 'duration': '1 hour'},
                    {'subject': 'Physics', 'time': '11:00 AM', 'duration': '1 hour'}
                ],
                'tuesday': [
                    {'subject': 'Chemistry', 'time': '10:00 AM', 'duration': '1 hour'},
                    {'subject': 'Computer Science', 'time': '2:00 PM', 'duration': '2 hours'}
                ]
            },
            'total_classes_per_week': 25
        }
        
        return timetable_data
        
    except Exception as e:
        print(f"Error processing timetable: {str(e)}")
        raise

@app.route('/generate-recommendations', methods=['POST'])
def generate_recommendations():
    try:
        data = request.json
        attendance_data = data.get('attendance_data', {})
        preferences = data.get('preferences', {})
        
        current_percentage = attendance_data.get('current_percentage', 0)
        target_percentage = 70.5
        
        recommendations = []
        
        # Generate recommendations based on attendance level
        if current_percentage > 80:
            recommendations.append({
                'type': 'optimization',
                'priority': 'low',
                'message': 'You have excellent attendance! You can strategically skip classes you dislike.',
                'suggested_actions': [
                    'Skip up to 2 classes of disliked subjects this week',
                    'Prioritize attending practical sessions',
                    'Use free time for extracurricular activities'
                ]
            })
        elif current_percentage > 75:
            recommendations.append({
                'type': 'balanced',
                'priority': 'medium',
                'message': 'Good attendance level. Be selective about which classes to skip.',
                'suggested_actions': [
                    'Skip only 1 class of least preferred subject',
                    'Attend all practical and important theory classes',
                    'Plan any trips carefully'
                ]
            })
        elif current_percentage > 70.5:
            recommendations.append({
                'type': 'caution',
                'priority': 'high',
                'message': 'You are in the safety zone but close to the limit. Avoid skipping classes.',
                'suggested_actions': [
                    'Attend all classes for the next 2 weeks',
                    'Postpone any planned trips',
                    'Focus on improving attendance'
                ]
            })
        else:
            recommendations.append({
                'type': 'critical',
                'priority': 'critical',
                'message': 'URGENT: Your attendance is below the safety threshold!',
                'suggested_actions': [
                    'Attend every single class without exception',
                    'Cancel any planned absences',
                    'Speak with your academic advisor immediately'
                ]
            })
        
        return jsonify({
            "success": True,
            "recommendations": recommendations,
            "safety_status": "safe" if current_percentage > 75 else "warning" if current_percentage > 70.5 else "critical"
        })
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return jsonify({"error": f"Failed to generate recommendations: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting AI Service (Lightweight Mode)...")
    print("Note: Heavy ML models disabled for faster startup")
    app.run(debug=True, port=5001, host='0.0.0.0')