import os
import requests
from transformers import pipeline
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

# Initialize Hugging Face models
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

text_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

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
        
        # Analyze sentiment for each preference
        sentences = preferences_text.split('.')
        analyzed_preferences = {
            'liked_subjects': [],
            'disliked_subjects': [],
            'liked_times': [],
            'disliked_times': [],
            'general_sentiment': 'neutral'
        }
        
        subject_keywords = [
            'mathematics', 'math', 'physics', 'chemistry', 'biology', 
            'computer science', 'programming', 'history', 'english',
            'literature', 'economics', 'sociology', 'psychology'
        ]
        
        time_keywords = [
            'morning', 'afternoon', 'evening', 'early morning', 
            'late evening', '8 am', '9 am', '10 am', 'monday', 'friday'
        ]
        
        for sentence in sentences:
            if sentence.strip():
                # Sentiment analysis
                sentiment_result = sentiment_analyzer(sentence)
                sentiment_score = sentiment_result[0]
                
                # Subject classification
                subject_classification = text_classifier(
                    sentence, 
                    subject_keywords,
                    hypothesis_template="This text is about {}."
                )
                
                # Time classification
                time_classification = text_classifier(
                    sentence,
                    time_keywords,
                    hypothesis_template="This text mentions {}."
                )
                
                # Extract preferences based on sentiment
                if sentiment_score['label'] == 'LABEL_2':  # Positive
                    # Add to liked categories
                    if subject_classification['scores'][0] > 0.5:
                        analyzed_preferences['liked_subjects'].append(
                            subject_classification['labels'][0]
                        )
                    if time_classification['scores'][0] > 0.5:
                        analyzed_preferences['liked_times'].append(
                            time_classification['labels'][0]
                        )
                        
                elif sentiment_score['label'] == 'LABEL_0':  # Negative
                    # Add to disliked categories
                    if subject_classification['scores'][0] > 0.5:
                        analyzed_preferences['disliked_subjects'].append(
                            subject_classification['labels'][0]
                        )
                    if time_classification['scores'][0] > 0.5:
                        analyzed_preferences['disliked_times'].append(
                            time_classification['labels'][0]
                        )
        
        # Remove duplicates
        analyzed_preferences['liked_subjects'] = list(set(analyzed_preferences['liked_subjects']))
        analyzed_preferences['disliked_subjects'] = list(set(analyzed_preferences['disliked_subjects']))
        analyzed_preferences['liked_times'] = list(set(analyzed_preferences['liked_times']))
        analyzed_preferences['disliked_times'] = list(set(analyzed_preferences['disliked_times']))
        
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
        # Convert PDF to image or load image
        if file_path.lower().endswith('.pdf'):
            # For PDF processing, you might need pdf2image
            # For now, we'll assume it's converted to image
            image = cv2.imread(file_path)
        else:
            image = cv2.imread(file_path)
        
        if image is None:
            raise Exception("Could not load image")
        
        # Preprocess image for better OCR
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(processed)
        
        # Parse calendar data
        calendar_data = parse_calendar_text(extracted_text)
        
        return calendar_data
        
    except Exception as e:
        print(f"Error processing calendar: {str(e)}")
        raise

def process_timetable_document(file_path):
    """Extract timetable information from PDF/image"""
    try:
        # Load and preprocess image
        image = cv2.imread(file_path)
        if image is None:
            raise Exception("Could not load image")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Extract text
        extracted_text = pytesseract.image_to_string(processed)
        
        # Parse timetable data
        timetable_data = parse_timetable_text(extracted_text)
        
        return timetable_data
        
    except Exception as e:
        print(f"Error processing timetable: {str(e)}")
        raise

def parse_calendar_text(text):
    """Parse calendar text to extract working days, holidays, etc."""
    calendar_data = {
        'semester_start': None,
        'semester_end': None,
        'holidays': [],
        'total_working_days': 0,
        'exam_dates': []
    }
    
    # Extract dates using regex
    date_patterns = [
        r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b',  # DD/MM/YYYY or DD-MM-YYYY
        r'\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b',  # YYYY/MM/DD or YYYY-MM-DD
    ]
    
    dates_found = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        dates_found.extend(matches)
    
    # Extract holiday information
    holiday_keywords = ['holiday', 'vacation', 'break', 'closed', 'festival']
    lines = text.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in holiday_keywords):
            calendar_data['holidays'].append(line.strip())
    
    # Estimate working days (this is a simplified calculation)
    if dates_found:
        calendar_data['total_working_days'] = max(100, len(dates_found) * 5)  # Rough estimate
    
    return calendar_data

def parse_timetable_text(text):
    """Parse timetable text to extract subject schedules"""
    timetable_data = {
        'subjects': [],
        'weekly_schedule': {},
        'total_classes_per_week': 0
    }
    
    # Common subject keywords
    subject_keywords = [
        'mathematics', 'math', 'physics', 'chemistry', 'biology',
        'computer science', 'programming', 'history', 'english',
        'literature', 'economics', 'lab', 'practical'
    ]
    
    # Time patterns
    time_pattern = r'\b(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)?\b'
    
    lines = text.split('\n')
    current_day = None
    
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
    for line in lines:
        line_clean = line.strip().lower()
        
        # Check if line contains a day of the week
        for day in days_of_week:
            if day in line_clean:
                current_day = day
                timetable_data['weekly_schedule'][day] = []
                break
        
        # Extract subjects and times
        if current_day:
            times = re.findall(time_pattern, line)
            for keyword in subject_keywords:
                if keyword in line_clean:
                    if keyword not in timetable_data['subjects']:
                        timetable_data['subjects'].append(keyword)
                    
                    class_info = {
                        'subject': keyword,
                        'day': current_day,
                        'times': times,
                        'raw_text': line.strip()
                    }
                    timetable_data['weekly_schedule'][current_day].append(class_info)
    
    # Calculate total classes per week
    total_classes = sum(len(day_schedule) for day_schedule in timetable_data['weekly_schedule'].values())
    timetable_data['total_classes_per_week'] = total_classes
    
    return timetable_data

@app.route('/generate-recommendations', methods=['POST'])
def generate_recommendations():
    try:
        data = request.json
        attendance_data = data.get('attendance_data', {})
        preferences = data.get('preferences', {})
        
        current_percentage = attendance_data.get('current_percentage', 0)
        target_percentage = 70.5
        
        recommendations = []
        
        # Generate AI-powered recommendations
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
    print("Starting AI Service...")
    print("Installing required models...")
    
    # Pre-load models to avoid delays
    try:
        sentiment_analyzer("test")
        text_classifier("test", ["test"])
        print("Models loaded successfully!")
    except Exception as e:
        print(f"Warning: Could not pre-load models: {e}")
    
    app.run(debug=True, port=5001, host='0.0.0.0')