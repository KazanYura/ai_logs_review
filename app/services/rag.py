# app/services/rag.py

import numpy as np
from .embedding_service import get_embedding_service
from .vector_search import LogVectorStore

try:
    from gpt4all import GPT4All
except ImportError:
    GPT4All = None

class LogRAGService:
    def __init__(self, log_id: int, embedding_model_name='all-MiniLM-L6-v2', vector_dim=384):
        print(f"Initializing RAG service for log_id: {log_id}")
        self._embedding_service = get_embedding_service()
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
        query_embedding = self._embedding_service.encode([query])[0]
        return self._vector_store.search(query_embedding, top_k=top_k)

    def ask_reasoner_v1(self, question: str, context_chunks: list[str], max_tokens: int = 1024) -> str:
        if self._reasoner_model is None:
            raise RuntimeError("GPT4All model not loaded.")
        if not context_chunks:
            return "Based on the provided logs, there is not enough information to answer that question."
        context = "\n".join(context_chunks)
        prompt_template = f"""
        <|system|>
        You are a Senior Site Reliability Engineer AI.
        Your job is to **find and clearly describe distinct, actionable issues** in the provided logs.
        Ignore informational or repetitive messages that do not indicate a malfunction.

        Follow these rules:
        - Only count something as an "issue" if it shows an **error**, **failure**, **exception**, **timeout**, or a **warning** that could cause system malfunction.
        - Group related log lines into one issue instead of listing duplicates separately.
        - If multiple issues share the same root cause, merge them into one.
        - If there are no actionable issues, clearly state: "No actionable issues found in the logs."

        For each issue found, provide:
        1. **Summary** – 1 short sentence describing the issue.
        2. **Evidence** – quote the most relevant log line(s) (keep only what's needed to prove the problem).
        3. **Recommendation** – the next step to investigate or fix it.

        Start your answer with:
        "Total distinct actionable issues: X"

        Separate each issue with `---`.
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