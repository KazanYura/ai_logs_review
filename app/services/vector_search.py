# app/services/vector_search.py

import faiss
import numpy as np
import json
import os

class LogVectorStore:
    """
    Manages a Faiss vector index and its corresponding text documents for a single log file.
    Can save itself to disk and load itself back based on a log_id.
    """
    def __init__(self, dim: int, log_id: int = None, base_path: str = "indexes"):
        self.dim = dim
        self.log_id = log_id
        self.base_path = base_path
        
        if log_id:
            self._load()
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.texts = []

    def add(self, embeddings: np.ndarray, texts: list[str]):
        embeddings_np = np.array(embeddings, dtype='float32')
        self.index.add(embeddings_np)
        self.texts.extend(texts)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[str]:
        if self.index.ntotal == 0:
            return []
        query_embedding_np = np.array([query_embedding], dtype='float32')
        distances, indices = self.index.search(query_embedding_np, top_k)
        return [self.texts[i] for i in indices[0] if i != -1]

    def save(self):
        """Saves the index and documents to disk using the instance's log_id."""
        if not self.log_id:
            raise ValueError("A log_id must be set to save the index.")
        
        os.makedirs(self.base_path, exist_ok=True)
        index_path = os.path.join(self.base_path, f"{self.log_id}.faiss")
        docs_path = os.path.join(self.base_path, f"{self.log_id}_docs.json")

        faiss.write_index(self.index, index_path)
        with open(docs_path, 'w', encoding='utf-8') as f:
            json.dump(self.texts, f)
        print(f"Saved index and documents for log_id {self.log_id}")

    def _load(self):
        """Loads the index and documents from disk using the instance's log_id."""
        index_path = os.path.join(self.base_path, f"{self.log_id}.faiss")
        docs_path = os.path.join(self.base_path, f"{self.log_id}_docs.json")

        if os.path.exists(index_path) and os.path.exists(docs_path):
            self.index = faiss.read_index(index_path)
            with open(docs_path, 'r', encoding='utf-8') as f:
                self.texts = json.load(f)
            print(f"Successfully loaded index for log_id {self.log_id}")
        else:
            print(f"No pre-built index found for log_id {self.log_id}. Starting fresh.")
            self.index = faiss.IndexFlatL2(self.dim)
            self.texts = []