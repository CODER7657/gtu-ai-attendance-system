'use client';

import React from 'react';
import AIChat from '@/components/chat/AIChat';
import { MessageCircle, Brain, Zap } from 'lucide-react';

const ChatPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <MessageCircle className="w-12 h-12 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">AI Chat Assistant</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Chat with your intelligent attendance assistant powered by Gemini 2.5 Pro. 
            Get personalized insights, strategies, and answers based on your analyzed data.
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <div className="flex items-center mb-3">
              <Brain className="w-8 h-8 text-purple-600 mr-3" />
              <h3 className="text-lg font-semibold text-gray-800">Smart Analysis</h3>
            </div>
            <p className="text-gray-600">
              AI understands your complete attendance data, preferences, and behavioral patterns 
              to provide personalized insights and recommendations.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <div className="flex items-center mb-3">
              <Zap className="w-8 h-8 text-yellow-600 mr-3" />
              <h3 className="text-lg font-semibold text-gray-800">Instant Answers</h3>
            </div>
            <p className="text-gray-600">
              Ask questions about your attendance status, get strategy suggestions, 
              or receive motivational support - all with immediate AI-powered responses.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <div className="flex items-center mb-3">
              <MessageCircle className="w-8 h-8 text-green-600 mr-3" />
              <h3 className="text-lg font-semibold text-gray-800">Contextual Chat</h3>
            </div>
            <p className="text-gray-600">
              Natural conversation with an AI that remembers your data and previous questions, 
              providing increasingly helpful and personalized assistance.
            </p>
          </div>
        </div>

        {/* Sample Questions */}
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Try asking questions like:</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <p className="text-gray-700">💡 "What's my current attendance status?"</p>
              <p className="text-gray-700">📊 "Which subjects need more attention?"</p>
              <p className="text-gray-700">🎯 "How can I improve my attendance strategy?"</p>
              <p className="text-gray-700">📈 "Show me my attendance trends over time"</p>
            </div>
            <div className="space-y-2">
              <p className="text-gray-700">⚡ "What's the optimal attendance for my liked subjects?"</p>
              <p className="text-gray-700">🔍 "Analyze my attendance patterns"</p>
              <p className="text-gray-700">💪 "Give me motivation to attend classes"</p>
              <p className="text-gray-700">🎓 "Help me balance attendance and study time"</p>
            </div>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="bg-white rounded-lg shadow-lg border border-gray-200" style={{ height: '600px' }}>
          <AIChat className="h-full" />
        </div>

        {/* Footer Info */}
        <div className="text-center mt-8">
          <div className="bg-blue-50 rounded-lg p-4 inline-block">
            <p className="text-blue-800 font-medium">
              🤖 Powered by Gemini 2.5 Pro with access to all your analyzed attendance data
            </p>
            <p className="text-blue-600 text-sm mt-1">
              Your conversations are processed securely and help improve personalized recommendations
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;