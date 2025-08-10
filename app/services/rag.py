from sentence_transformers import SentenceTransformer
from .vector_search import LogVectorStore
import numpy as np

try:
    from gpt4all import GPT4All
except ImportError:
    GPT4All = None

class LogRAGService:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2', vector_dim=384):
        self._model = SentenceTransformer(embedding_model_name)
        self._vector_store = LogVectorStore(dim=vector_dim)
        self._reasoner_model = None
        if GPT4All:
            try:
                self._reasoner_model = GPT4All("qwen2.5-coder-7b-instruct-q4_0.gguf")
            except Exception as e:
                print(f"Could not load GPT4All model: {e}")

    def add_logs(self, log_chunks):
        if not log_chunks: # Guard against empty input
            return
        embeddings = self._embed_texts(log_chunks)
        self._vector_store.add(embeddings, log_chunks)

    def retrieve_logs(self, query, top_k=5):
        """
        Public API: Retrieve top_k relevant log chunks for a query.
        """
        # Guard against empty queries
        if not query:
            return []
        embeddings = self._embed_texts([query])
        
        if embeddings.shape[0] == 0:
            return []
        query_emb = embeddings[0]
        return self._vector_store.search(query_emb, top_k=top_k)

    def ask_reasoner(self, question, context_chunks, max_tokens=256):
        if self._reasoner_model is None:
            raise RuntimeError("GPT4All is not installed or the model could not be loaded.")
        
        if not context_chunks:
            return "I could not find any relevant logs to answer your question."

        context = "\n".join(context_chunks)
        prompt_template = f"""
        <|system|>
        You are an expert AI assistant specialized in analyzing log data. Use the following log entries to answer the user's question. Provide a concise and direct answer based only on the given context.
        </s>
        <|user|>
        Context:
        {context}

        Question: {question}
        </s>
        <|assistant|>
        """
        response = self._reasoner_model.generate(prompt_template.strip(), max_tokens=max_tokens)
        return response

    def retrieve_relevant_logs(self, query, top_k=5):
        return self.retrieve_logs(query, top_k=top_k)

    def ask_reasoner_v1(self, question, context_chunks, max_tokens=256):
        return self.ask_reasoner(question, context_chunks, max_tokens=max_tokens)

    def _embed_texts(self, texts):
        return self._model.encode(texts, convert_to_numpy=True)