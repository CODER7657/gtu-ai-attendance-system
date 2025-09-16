import requests
import json

def test_chat_functionality():
    """Test the AI Chat system with various questions"""
    
    print("🧪 Testing AI Chat Assistant")
    print("=" * 50)
    
    # Test questions covering different aspects
    test_questions = [
        "Hello! What can you help me with?",
        "What's my current attendance status?",
        "Which subjects need more attention?",
        "How can I improve my attendance strategy?",
        "Give me some motivation to attend classes regularly",
        "What are the benefits of maintaining good attendance?"
    ]
    
    backend_url = "http://localhost:5000"
    ai_service_url = "http://localhost:5001"
    
    # Check if services are running
    try:
        backend_health = requests.get(f"{backend_url}/health", timeout=5)
        print("✅ Backend server is running")
    except requests.exceptions.RequestException:
        print("❌ Backend server not available")
        return False
        
    try:
        ai_health = requests.get(f"{ai_service_url}/health", timeout=5)
        print("✅ AI service is running")
        ai_status = ai_health.json()
        print(f"🤖 Model: {ai_status.get('model', 'Unknown')}")
    except requests.exceptions.RequestException:
        print("❌ AI service not available")
        return False
    
    print("\n🎯 Testing Chat Conversations:")
    print("=" * 40)
    
    # Test each question
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 💬 User: {question}")
        
        try:
            # Test the backend chat endpoint
            response = requests.post(
                f"{backend_url}/api/chat",
                json={
                    "message": question,
                    "context": {
                        "conversation_id": f"test_{i}",
                        "test_mode": True
                    }
                },
                timeout=30  # Generous timeout for AI processing
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"✅ 🤖 AI Response: {data.get('response', 'No response')[:150]}...")
                    
                    if data.get("suggestions"):
                        print(f"💡 Suggestions: {', '.join(data['suggestions'][:3])}")
                    
                    print(f"📊 Processing: {data.get('processing_method', 'unknown')}")
                else:
                    print(f"⚠️ Response not successful: {data}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out (AI processing may be slow)")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Chat functionality testing completed!")
    print("📝 Note: If responses show 'fallback' processing, Gemini API may be at quota limit")
    print("💡 Try accessing http://localhost:3000/chat to test the web interface")
    
    return True

if __name__ == "__main__":
    test_chat_functionality()