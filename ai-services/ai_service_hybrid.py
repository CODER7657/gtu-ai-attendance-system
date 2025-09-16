import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime
import json
import time

app = Flask(__name__)
CORS(app)

# Initialize models with error handling and retries
sentiment_analyzer = None
text_classifier = None

def initialize_models():
    """Initialize AI models with retries and fallbacks"""
    global sentiment_analyzer, text_classifier
    
    print("🤖 Initializing AI models...")
    
    try:
        print("📥 Loading sentiment analysis model...")
        from transformers import pipeline
        
        # Try smaller, faster models first
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        print("✅ Sentiment analyzer loaded!")
        
        print("📥 Loading text classifier...")
        text_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        print("✅ Text classifier loaded!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        print("🔄 Falling back to lightweight mode...")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "AI service is running",
        "models_loaded": sentiment_analyzer is not None and text_classifier is not None
    })

@app.route('/process-preferences', methods=['POST'])
def process_preferences():
    try:
        data = request.json
        preferences_text = data.get('preferences', '')
        
        if not preferences_text:
            return jsonify({"error": "No preferences provided"}), 400
        
        if sentiment_analyzer and text_classifier:
            # Use real AI models
            return process_preferences_with_ai(preferences_text)
        else:
            # Use keyword-based fallback
            return process_preferences_with_keywords(preferences_text)
        
    except Exception as e:
        print(f"Error processing preferences: {str(e)}")
        return jsonify({"error": f"Failed to process preferences: {str(e)}"}), 500

def process_preferences_with_ai(preferences_text):
    """Process preferences using real AI models"""
    print("🧠 Using AI models for preference analysis...")
    
    analyzed_preferences = {
        'liked_subjects': [],
        'disliked_subjects': [],
        'liked_times': [],
        'disliked_times': [],
        'general_sentiment': 'neutral',
        'confidence_score': 0.0,
        'processing_method': 'AI_MODELS'
    }
    
    # Split into sentences for analysis
    sentences = preferences_text.split('.')
    
    subject_keywords = [
        'mathematics', 'math', 'physics', 'chemistry', 'biology', 
        'computer science', 'programming', 'history', 'english',
        'literature', 'economics', 'sociology', 'psychology'
    ]
    
    time_keywords = [
        'morning', 'afternoon', 'evening', 'early morning', 
        'late evening', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'
    ]
    
    total_confidence = 0
    sentence_count = 0
    
    for sentence in sentences:
        if sentence.strip():
            sentence_count += 1
            
            # AI Sentiment analysis
            sentiment_result = sentiment_analyzer(sentence)
            sentiment_score = sentiment_result[0]
            confidence = sentiment_score['score']
            total_confidence += confidence
            
            # AI Subject classification
            subject_classification = text_classifier(
                sentence, 
                subject_keywords,
                hypothesis_template="This text is about {}."
            )
            
            # AI Time classification
            time_classification = text_classifier(
                sentence,
                time_keywords,
                hypothesis_template="This text mentions {}."
            )
            
            # Extract preferences based on AI sentiment
            if sentiment_score['label'] in ['LABEL_2', 'POSITIVE'] and confidence > 0.6:
                # Positive sentiment - liked items
                if subject_classification['scores'][0] > 0.3:
                    subject = subject_classification['labels'][0]
                    if subject not in analyzed_preferences['liked_subjects']:
                        analyzed_preferences['liked_subjects'].append(subject)
                
                if time_classification['scores'][0] > 0.3:
                    time_slot = time_classification['labels'][0]
                    if time_slot not in analyzed_preferences['liked_times']:
                        analyzed_preferences['liked_times'].append(time_slot)
                        
            elif sentiment_score['label'] in ['LABEL_0', 'NEGATIVE'] and confidence > 0.6:
                # Negative sentiment - disliked items
                if subject_classification['scores'][0] > 0.3:
                    subject = subject_classification['labels'][0]
                    if subject not in analyzed_preferences['disliked_subjects']:
                        analyzed_preferences['disliked_subjects'].append(subject)
                
                if time_classification['scores'][0] > 0.3:
                    time_slot = time_classification['labels'][0]
                    if time_slot not in analyzed_preferences['disliked_times']:
                        analyzed_preferences['disliked_times'].append(time_slot)
    
    # Calculate average confidence
    analyzed_preferences['confidence_score'] = total_confidence / max(sentence_count, 1)
    
    return jsonify({
        "success": True,
        "analyzed_preferences": analyzed_preferences,
        "original_text": preferences_text
    })

def process_preferences_with_keywords(preferences_text):
    """Fallback: Process preferences using keyword matching"""
    print("🔤 Using keyword-based analysis (fallback mode)...")
    
    analyzed_preferences = {
        'liked_subjects': [],
        'disliked_subjects': [],
        'liked_times': [],
        'disliked_times': [],
        'general_sentiment': 'neutral',
        'confidence_score': 0.7,  # Medium confidence for keyword matching
        'processing_method': 'KEYWORD_BASED'
    }
    
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
    
    time_keywords = {
        'morning': ['morning', '8 am', '9 am', '10 am'],
        'afternoon': ['afternoon', '12 pm', '1 pm', '2 pm'],
        'evening': ['evening', '4 pm', '5 pm', '6 pm'],
        'early_morning': ['early morning', '7 am', '6 am']
    }
    
    # Sentiment words
    positive_words = ['love', 'like', 'enjoy', 'prefer', 'favorite', 'best', 'good', 'great', 'excellent']
    negative_words = ['hate', 'dislike', 'boring', 'worst', 'bad', 'terrible', 'awful', 'avoid']
    
    sentences = preferences_text.split('.')
    
    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        if not sentence_lower:
            continue
            
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

@app.route('/model-status', methods=['GET'])
def model_status():
    """Check which AI models are loaded"""
    return jsonify({
        "sentiment_analyzer": sentiment_analyzer is not None,
        "text_classifier": text_classifier is not None,
        "mode": "AI_MODELS" if (sentiment_analyzer and text_classifier) else "KEYWORD_BASED"
    })

if __name__ == '__main__':
    print("🚀 Starting Enhanced AI Service...")
    
    # Try to initialize models
    models_loaded = initialize_models()
    
    if models_loaded:
        print("✅ AI models ready! Using advanced ML processing.")
    else:
        print("⚠️  Running in fallback mode with keyword-based processing.")
    
    print("🌐 Starting Flask server...")
    app.run(debug=True, port=5001, host='0.0.0.0')