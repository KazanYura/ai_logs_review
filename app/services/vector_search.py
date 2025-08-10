import faiss
import numpy as np

class LogVectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        embeddings_np = np.array(embeddings, dtype='float32')
        self.index.add(embeddings_np)
        self.texts.extend(texts)

    def search(self, query_embedding, top_k=5):
        if self.index.ntotal == 0:
            return []

        query_embedding_np = np.array([query_embedding], dtype='float32')
        distances, indices = self.index.search(query_embedding_np, top_k)

        results = [self.texts[i] for i in indices[0] if i != -1]
        
        return results