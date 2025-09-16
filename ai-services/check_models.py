import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Checking available Gemini models...")

try:
    # List all available models
    models = genai.list_models()
    
    print("\n📋 Available Gemini Models:")
    print("=" * 50)
    
    latest_models = []
    for model in models:
        model_name = model.name.replace('models/', '')
        if 'gemini' in model_name.lower():
            print(f"✅ {model_name}")
            if 'gemini-1.5' in model_name or 'gemini-2' in model_name:
                latest_models.append(model_name)
    
    print(f"\n🚀 Latest Generation Models:")
    print("=" * 30)
    for model in latest_models:
        print(f"⭐ {model}")
    
    # Test the latest model
    if latest_models:
        latest_model = latest_models[0]  # Get the first latest model
        print(f"\n🧪 Testing latest model: {latest_model}")
        
        try:
            test_model = genai.GenerativeModel(latest_model)
            response = test_model.generate_content("Hello! What model are you?")
            print(f"✅ Model Response: {response.text[:100]}...")
            print(f"🎯 Recommended model: {latest_model}")
        except Exception as e:
            print(f"❌ Error testing {latest_model}: {str(e)}")
            print("🔄 Falling back to gemini-1.5-pro")
    
except Exception as e:
    print(f"❌ Error accessing Gemini API: {str(e)}")
    print("🔑 Please check your API key and quota status")