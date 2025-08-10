# app/api/router.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.base import ChatRequest, ChatResponse
from app.services.log_processor import LogProcessor
from app.services.rag import LogRAGService
from app.db.crud import get_log_lines_by_id

router = APIRouter()
processor = LogProcessor()

GENERIC_KEYWORDS = ['error', 'fail', 'issue', 'problem', 'summarize', 'what went wrong']

@router.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode('utf-8')
    processed_entries, log_id = await processor.process_and_index_log_file(text)
    if not log_id:
        raise HTTPException(status_code=400, detail="No valid log entries found to process.")
    return {"message": "File processed and indexed successfully.", "log_id": log_id}

@router.post("/chat", response_model=ChatResponse)
async def chat_logs(request: ChatRequest):
    try:
        full_log_content = await get_log_lines_by_id(log_id=request.log_id)
        if not full_log_content:
            return ChatResponse(answer=f"No logs found for ID {request.log_id}.", context=[])
            
        rag_service = LogRAGService(log_id=request.log_id)
        
        context_chunks = []
        is_generic = any(keyword in request.question.lower() for keyword in GENERIC_KEYWORDS)

        if is_generic:
            context_chunks = [line.message for line in full_log_content if line.level in ["ERROR", "CRITICAL", "FATAL"]]
        else:
            context_chunks = rag_service.retrieve_relevant_logs(request.question, top_k=request.top_k)
            if not context_chunks:
                print(f"Specific search for log_id {request.log_id} found no results. Falling back to error filtering.")
                context_chunks = [line.message for line in full_log_content if line.level in ["ERROR", "CRITICAL", "FATAL"]]
        
        answer = rag_service.ask_reasoner_v1(request.question, context_chunks)
        return ChatResponse(answer=answer, context=context_chunks)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))