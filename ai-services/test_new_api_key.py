import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
genai.configure(api_key=GEMINI_API_KEY)

print("🔑 Testing new Gemini API key...")
print(f"API Key (first 10 chars): {GEMINI_API_KEY[:10]}...")

try:
    # Test with Gemini 2.5 Pro
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content("Hello! This is a test to verify the new API key is working. Please respond with 'API key is working successfully!'")
    print(f"✅ Success! Response: {response.text}")
    
    # Test chat functionality
    chat_response = model.generate_content("I'm a student with 75% attendance. Should I be worried?")
    print(f"✅ Chat test: {chat_response.text[:100]}...")
    
    print("🎉 New API key is working perfectly!")
    
except Exception as e:
    print(f"❌ Error with new API key: {str(e)}")
    
    # Try fallback model
    try:
        print("🔄 Trying fallback model...")
        fallback_model = genai.GenerativeModel('gemini-1.5-pro')
        response = fallback_model.generate_content("Test fallback")
        print(f"✅ Fallback works: {response.text[:50]}...")
    except Exception as e2:
        print(f"❌ Fallback also failed: {str(e2)}")