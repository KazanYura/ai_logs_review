import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, Bot, User } from 'lucide-react';
import { logsApi } from '../api';

const ChatInterface = ({ logId, fileName }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Reset messages when log ID changes
    setMessages([]);
  }, [logId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || !logId) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await logsApi.chatWithLogs(userMessage.content, logId);
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.answer,
        context: response.context,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatMessage = (content) => {
    // Simple formatting for structured responses
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n\n/g, '\n')
      .split('\n')
      .map((line, index) => (
        <div key={index} dangerouslySetInnerHTML={{ __html: line }} />
      ));
  };

  const suggestedQuestions = [
    "What errors occurred in this log?",
    "Summarize the main issues",
    "What went wrong?",
    "Show me critical problems",
    "Analyze the log for anomalies"
  ];

  const handleSuggestedQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <div className="chat-section">
      <h2 className="section-title">
        <MessageCircle className="w-6 h-6" />
        Chat with AI
        {fileName && <span className="text-sm font-normal text-gray-500">({fileName})</span>}
      </h2>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-placeholder">
            {logId ? (
              <div>
                <p>Ask me anything about your log file!</p>
                <div className="mt-4">
                  <p className="text-sm font-medium mb-2">Try these questions:</p>
                  <div className="flex flex-wrap gap-2">
                    {suggestedQuestions.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => handleSuggestedQuestion(question)}
                        className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
                      >
                        {question}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              'Upload a log file to start chatting with the AI'
            )}
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.type}`}>
                <div className="message-label">
                  {message.type === 'user' ? (
                    <>
                      <User className="w-4 h-4 inline mr-1" />
                      You
                    </>
                  ) : (
                    <>
                      <Bot className="w-4 h-4 inline mr-1" />
                      AI Assistant
                    </>
                  )}
                </div>
                <div className="message-content">
                  {message.type === 'assistant' ? (
                    <>
                      <div className={message.isError ? 'error-message' : ''}>
                        {formatMessage(message.content)}
                      </div>
                      {message.context && message.context.length > 0 && (
                        <div className="context-section">
                          <div className="context-title">
                            Relevant Log Context ({message.context.length} entries):
                          </div>
                          <div className="context-items">
                            {message.context.slice(0, 3).map((item, index) => (
                              <div key={index} className="mb-1">
                                • {item.substring(0, 200)}
                                {item.length > 200 ? '...' : ''}
                              </div>
                            ))}
                            {message.context.length > 3 && (
                              <div className="text-xs italic">
                                ... and {message.context.length - 3} more entries
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </>
                  ) : (
                    message.content
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-label">
                  <Bot className="w-4 h-4 inline mr-1" />
                  AI Assistant
                </div>
                <div className="flex items-center gap-2">
                  <div className="loading-spinner" />
                  Analyzing logs...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={logId ? "Ask about your logs..." : "Upload a log file first"}
          className="chat-input"
          disabled={!logId || isLoading}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!logId || !inputValue.trim() || isLoading}
        >
          {isLoading ? (
            <div className="loading-spinner" />
          ) : (
            <Send className="w-4 h-4" />
          )}
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
