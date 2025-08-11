import React, { useState } from 'react';
import LogUpload from './components/LogUpload';
import ChatInterface from './components/ChatInterface';
import { Brain } from 'lucide-react';

function App() {
  const [currentLogId, setCurrentLogId] = useState(null);
  const [currentFileName, setCurrentFileName] = useState(null);

  const handleUploadSuccess = (logId, fileName) => {
    setCurrentLogId(logId);
    setCurrentFileName(fileName);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>
          <Brain className="inline-block w-10 h-10 mr-3" />
          AI Logs Review
        </h1>
        <p>Upload your log files and chat with AI to analyze issues and get insights</p>
      </header>

      <main className="main-content">
        <LogUpload onUploadSuccess={handleUploadSuccess} />
        <ChatInterface logId={currentLogId} fileName={currentFileName} />
      </main>

      {currentLogId && (
        <div style={{ 
          position: 'fixed', 
          bottom: '20px', 
          right: '20px', 
          background: '#10b981', 
          color: 'white', 
          padding: '8px 16px', 
          borderRadius: '20px', 
          fontSize: '14px',
          fontWeight: '500',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
        }}>
          Log ID: {currentLogId} • Ready to chat!
        </div>
      )}
    </div>
  );
}

export default App;
