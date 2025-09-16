'use client';

import React, { useState, useEffect, useRef } from 'react';
import './AIChat.css';
import { apiService } from '../../services/api';
import { Send, MessageSquare, Bot, User, Lightbulb, Clock, TrendingUp } from 'lucide-react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  suggestions?: string[];
}

interface ChatProps {
  className?: string;
}

const AIChat: React.FC<ChatProps> = ({ className = '' }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm your AI Attendance Assistant. I have access to all your analyzed attendance data and preferences. Ask me anything about your attendance patterns, strategies, or get personalized advice!",
      sender: 'ai',
      timestamp: new Date(),
      suggestions: [
        "What's my current attendance status?",
        "Which subjects need more attention?",
        "How can I improve my attendance strategy?",
        "Show me my attendance trends"
      ]
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const data = await apiService.sendChatMessage(messageText, {
        conversation_id: 'main',
        previous_messages: messages.slice(-5) // Send last 5 messages for context
      });

      if (data.success) {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: data.response,
          sender: 'ai',
          timestamp: new Date(),
          suggestions: data.suggestions || []
        };

        setTimeout(() => {
          setMessages(prev => [...prev, aiMessage]);
          setIsTyping(false);
        }, 500); // Simulate typing delay
      } else {
        throw new Error(data.error || 'Failed to get AI response');
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm having trouble connecting right now. Please try again in a moment, or ask me about basic attendance topics.",
        sender: 'ai',
        timestamp: new Date(),
        suggestions: [
          "What's the minimum attendance requirement?",
          "Give me general attendance tips",
          "How to calculate attendance percentage?",
          "Best practices for class attendance"
        ]
      };
      setTimeout(() => {
        setMessages(prev => [...prev, errorMessage]);
        setIsTyping(false);
      }, 500);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion);
  };

  const formatTime = (date: Date) => {
    // Use consistent format to avoid hydration mismatch
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  return (
    <div className={`flex flex-col h-full bg-white rounded-lg shadow-lg ${className}`}>
      {/* Chat Header */}
      <div className="flex items-center p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-t-lg">
        <Bot className="w-6 h-6 mr-3" />
        <div>
          <h3 className="font-semibold">AI Attendance Assistant</h3>
          <p className="text-sm opacity-90">Powered by Gemini 2.5 Pro</p>
        </div>
        <div className="ml-auto flex items-center">
          <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
          <span className="text-xs">Online</span>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl ${message.sender === 'user' ? 'order-2' : 'order-1'}`}>
              <div className={`flex items-start space-x-2 ${message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  message.sender === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                }`}>
                  {message.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>
                
                <div className={`rounded-lg p-3 ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white ml-auto'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  <p className="whitespace-pre-wrap">{message.text}</p>
                  <p className={`text-xs mt-1 ${
                    message.sender === 'user' ? 'text-blue-200' : 'text-gray-500'
                  }`}>
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
              
              {/* AI Suggestions */}
              {message.sender === 'ai' && message.suggestions && message.suggestions.length > 0 && (
                <div className="mt-3 ml-10">
                  <div className="flex items-center mb-2">
                    <Lightbulb className="w-4 h-4 text-yellow-500 mr-1" />
                    <span className="text-xs text-gray-600 font-medium">Suggested questions:</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {message.suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="px-3 py-1 text-xs bg-blue-50 text-blue-600 rounded-full border border-blue-200 hover:bg-blue-100 transition-colors"
                        disabled={isLoading}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {/* Typing Indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex items-start space-x-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-gray-100 rounded-lg p-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="px-4 py-2 border-t border-gray-200">
        <div className="flex items-center space-x-2 text-xs text-gray-600">
          <Clock className="w-3 h-3" />
          <span>Quick actions:</span>
          <button 
            onClick={() => handleSuggestionClick("What's my attendance summary?")}
            className="px-2 py-1 bg-gray-100 rounded hover:bg-gray-200 transition-colors"
            disabled={isLoading}
          >
            Summary
          </button>
          <button 
            onClick={() => handleSuggestionClick("Give me attendance tips")}
            className="px-2 py-1 bg-gray-100 rounded hover:bg-gray-200 transition-colors"
            disabled={isLoading}
          >
            Tips
          </button>
          <button 
            onClick={() => handleSuggestionClick("Show my trends")}
            className="px-2 py-1 bg-gray-100 rounded hover:bg-gray-200 transition-colors"
            disabled={isLoading}
          >
            <TrendingUp className="w-3 h-3 inline mr-1" />
            Trends
          </button>
        </div>
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-2">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask me anything about your attendance..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          💡 I have access to all your uploaded data and can provide personalized attendance insights
        </p>
      </form>
    </div>
  );
};

export default AIChat;