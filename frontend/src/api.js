import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 960000, // 30 seconds timeout for file uploads
});

export const logsApi = {
  // Upload a log file
  uploadLog: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/v1/logs/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  // Chat with the AI about logs
  chatWithLogs: async (question, logId, topK = 5) => {
    const response = await api.post('/v1/logs/chat', {
      question,
      log_id: logId,
      top_k: topK,
    });
    
    return response.data;
  },
};

export default api;
