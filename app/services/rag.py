# app/services/rag.py

import numpy as np
from sentence_transformers import SentenceTransformer
from .vector_search import LogVectorStore

try:
    from gpt4all import GPT4All
except ImportError:
    GPT4All = None

class LogRAGService:
    def __init__(self, log_id: int, embedding_model_name='all-MiniLM-L6-v2', vector_dim=384):
        print(f"Initializing RAG service for log_id: {log_id}")
        self._embedding_model = SentenceTransformer(embedding_model_name)
        self._reasoner_model = self._get_reasoner_model()
        self._vector_store = LogVectorStore(dim=vector_dim, log_id=log_id)

    def _get_reasoner_model(self):
        if not GPT4All: return None
        try:
            return GPT4All("qwen2.5-coder-7b-instruct-q4_0.gguf")
        except Exception as e:
            print(f"Could not load GPT4All model: {e}")
            return None
            
    def retrieve_relevant_logs(self, query: str, top_k: int = 5) -> list[str]:
        if not query or self._vector_store.index.ntotal == 0:
            return []
        query_embedding = self._embedding_model.encode([query])[0]
        return self._vector_store.search(query_embedding, top_k=top_k)

    def ask_reasoner_v1(self, question: str, context_chunks: list[str], max_tokens: int = 1024) -> str:
        if self._reasoner_model is None:
            raise RuntimeError("GPT4All model not loaded.")
        if not context_chunks:
            return "Based on the provided logs, there is not enough information to answer that question."
        context = "\n".join(context_chunks)
        prompt_template = f"""
        <|system|>
        You are a Senior Site Reliability Engineer AI. Your task is to analyze the provided log context and identify ALL distinct errors, warnings, and notable anomalies. Do not focus on just one issue.

        If the answer cannot be found, state that clearly.

        For EACH distinct issue you identify which is related to User's Question, structure your response with the following three parts:
        1.  **Summary:** A one-sentence summary of the specific issue.
        2.  **Evidence:** Quote the exact log line(s) that point to this issue.
        3.  **Recommendation:** Suggest a specific next step to investigate or fix this issue.

        Begin your response by stating the total number of distinct issues you found. Separate each issue with a horizontal line (---).
        </s>
        <|user|>
        ### Log Context Provided:
        {context}

        ### User's Question:
        {question}
        </s>
        <|assistant|>
        """
        return self._reasoner_model.generate(prompt_template.strip(), max_tokens=max_tokens)