# AI Logs Review

A robust AI-powered log analysis tool designed to help you upload, process, and interact with log files for efficient identification of issues, errors, and anomalies.

## Features

- **AI-Driven Analysis**: Leverage GPT4All for advanced log insights
- **Streamlined Upload**: Drag & drop log file upload and processing
- **Semantic Search**: Vector-based search through log entries
- **Conversational Interface**: Query logs using natural language
- **Contextual Retrieval**: Relevant log entries provided for precise answers
- **Data Privacy**: Automatic anonymization of sensitive data (emails, IPs, tokens)
- **High Performance**: Asynchronous FastAPI backend with SQLite
- **Modern UI**: Responsive React.js frontend

## Architecture

### Backend (FastAPI)
- **FastAPI** – High-performance web framework
- **SQLAlchemy** – Async ORM with SQLite
- **Sentence Transformers** – Text embeddings (`all-MiniLM-L6-v2`)
- **FAISS** – Vector similarity search
- **GPT4All** – Local LLM for reasoning (`qwen2.5-coder-7b-instruct`)

### Frontend (React.js)
- **React 18** – UI framework
- **Axios** – HTTP client
- **React Dropzone** – File upload component
- **Lucide React** – Icon library

## Installation

### Prerequisites
- Python 3.10+
- Node.js 14+
- Poetry (recommended) or pip

### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/KazanYura/ai_logs_review.git
cd ai_logs_review
```

2. **Install backend dependencies**:
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt  # Generate from pyproject.toml
```

3. **Install frontend dependencies**:
```bash
cd frontend
npm install
cd ..
```

4. **Start the development environment**:

**Windows:**
```bash
start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

**Manual start:**
```bash
# Terminal 1 - Backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

## Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Usage

1. **Upload a Log File**:
    - Open the web interface
    - Drag & drop or select a `.log` or `.txt` file
    - Wait for processing and indexing

2. **Interact with AI**:
    - Ask questions about your logs
    - Use suggested queries for analysis
    - Review AI responses with relevant log context

### Example Queries:
- "List errors in this log."
- "Summarize main issues."
- "Identify critical problems."
- "Analyze for anomalies."

## Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=sqlite+aiosqlite:///./logs.db
LOG_LEVEL=INFO
MAX_FILE_SIZE=50MB
```

### Supported Log Format
Expected log format:
```
[2024-01-01 12:00:00,123] [ERROR] Your log message here
[2024-01-01 12:00:01,456] [INFO] Another log message
```

## Development

### Project Structure
```
ai_logs_review/
├── app/
│   ├── api/v1/endpoints/     # API endpoints
│   ├── core/                 # Configuration
│   ├── db/                   # Database models & CRUD
│   ├── models/               # Pydantic models
│   └── services/             # Business logic
├── frontend/
│   ├── public/               # Static files
│   └── src/                  # React components
├── indexes/                  # FAISS vector indexes
├── main.py                   # Application entry point
└── pyproject.toml            # Python dependencies
```

### API Endpoints
- `POST /v1/logs/upload` – Upload and process log files
- `POST /v1/logs/chat` – Query logs via AI

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to your branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **GPT4All model not loading**:
    - Ensure sufficient disk space (~4GB)
    - Verify internet connection for initial download

2. **CORS errors**:
    - Confirm backend is running on port 8000
    - Check CORS settings in `app/__init__.py`

3. **File upload fails**:
    - Confirm file format (.log or .txt)
    - Check file size limits
    - Review backend logs for errors

## Planned Enhancements

- [ ] Additional log format support (JSON, XML)
- [ ] Real-time log streaming
- [ ] Advanced filtering and search
- [ ] User authentication and multi-tenancy
- [ ] Cloud deployment guides
- [ ] Analytics dashboard

---
