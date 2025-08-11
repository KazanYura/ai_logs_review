# AI Logs Review - Frontend

A modern React.js frontend for the AI Logs Review application that provides an intuitive interface for uploading log files and chatting with AI about log analysis.

## Features

- **Drag & Drop Upload**: Easy log file upload with visual feedback
- **Real-time Chat**: Interactive chat interface with AI assistant
- **Responsive Design**: Works on desktop and mobile devices
- **Suggested Questions**: Quick-start questions for log analysis
- **Context Display**: Shows relevant log entries used for AI responses
- **Beautiful UI**: Modern, clean interface with smooth animations

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- The AI Logs Review backend running on `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`.

### Usage

1. **Upload a Log File**: 
   - Drag and drop a `.log` or `.txt` file onto the upload area
   - Or click to select a file from your computer
   - Wait for the file to be processed and indexed

2. **Chat with AI**:
   - Once upload is complete, use the chat interface
   - Ask questions about your logs
   - Try suggested questions for quick analysis
   - View the AI's responses with relevant log context

### Example Questions

- "What errors occurred in this log?"
- "Summarize the main issues"
- "What went wrong?"
- "Show me critical problems"
- "Analyze the log for anomalies"

## API Integration

The frontend communicates with the FastAPI backend through:

- `POST /v1/logs/upload` - Upload and process log files
- `POST /v1/logs/chat` - Chat with AI about logs

## Building for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## Technology Stack

- **React 18** - Frontend framework
- **Axios** - HTTP client for API communication
- **React Dropzone** - File upload component
- **Lucide React** - Icon library
- **CSS3** - Styling with modern features

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
