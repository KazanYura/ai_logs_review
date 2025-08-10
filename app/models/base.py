from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5
    log_id: int

class ChatResponse(BaseModel):
    answer: str
    context: list[str]