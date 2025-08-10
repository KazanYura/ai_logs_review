from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.base import ChatRequest, ChatResponse
from app.services.log_processor import LogProcessor
from app.services.rag import LogRAGService

router = APIRouter()
processor = LogProcessor()
log_rag_service = LogRAGService()


@router.post("/chat", response_model=ChatResponse)
async def chat_logs(request: ChatRequest):
    try:
        context_chunks = log_rag_service.retrieve_relevant_logs(request.question, top_k=request.top_k)
        answer = log_rag_service.ask_reasoner_v1(request.question, context_chunks)
        return ChatResponse(answer=answer, context=context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode('utf-8')
    processed_entries = await processor.process_log_text(text)
    return {"processed_lines": [entry.dict() for entry in processed_entries]}


