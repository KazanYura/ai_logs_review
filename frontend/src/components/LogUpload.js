import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { logsApi } from '../api';

const LogUpload = ({ onUploadSuccess }) => {
  const [uploadStatus, setUploadStatus] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploadedFile(file);
    setUploadStatus({ type: 'uploading', message: 'Uploading and processing log file...' });

    try {
      const result = await logsApi.uploadLog(file);
      setUploadStatus({
        type: 'success',
        message: `File processed successfully! Log ID: ${result.log_id}`,
      });
      onUploadSuccess(result.log_id, file.name);
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Failed to upload file. Please try again.',
      });
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.log', '.txt'],
      'application/octet-stream': ['.log'],
    },
    maxFiles: 1,
  });

  const getStatusIcon = () => {
    switch (uploadStatus?.type) {
      case 'success':
        return <CheckCircle className="w-5 h-5" />;
      case 'error':
        return <AlertCircle className="w-5 h-5" />;
      case 'uploading':
        return <div className="loading-spinner" />;
      default:
        return null;
    }
  };

  return (
    <div className="upload-section">
      <h2 className="section-title">
        <Upload className="w-6 h-6" />
        Upload Log File
      </h2>
      
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="dropzone-content">
          <FileText className={`w-12 h-12 dropzone-icon`} />
          <p className="dropzone-text">
            {isDragActive
              ? 'Drop the log file here...'
              : 'Drag & drop a log file here, or click to select'}
          </p>
          <p className="dropzone-subtext">
            Supports .log and .txt files
          </p>
        </div>
      </div>

      {uploadedFile && (
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            Selected file: <span className="font-medium">{uploadedFile.name}</span>
          </p>
          <p className="text-sm text-gray-500">
            Size: {(uploadedFile.size / 1024).toFixed(2)} KB
          </p>
        </div>
      )}

      {uploadStatus && (
        <div className={`upload-status ${uploadStatus.type}`}>
          <div className="flex items-center gap-2">
            {getStatusIcon()}
            {uploadStatus.message}
          </div>
        </div>
      )}
    </div>
  );
};

export default LogUpload;
