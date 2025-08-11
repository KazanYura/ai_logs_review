"""
Lightweight embedding service that can work without PyTorch if needed.
Falls back to simple text processing if ML libraries are unavailable.
"""
import logging
from typing import List, Optional
import hashlib
import json

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service that handles text embeddings with fallback options."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
        self.use_ml = self._initialize_ml_model()
        
    def _initialize_ml_model(self) -> bool:
        """Try to initialize ML model, fall back to simple processing if failed."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info("SentenceTransformer model loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer: {e}")
            logger.info("Falling back to simple text processing")
            return False
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """Encode texts to embeddings, with fallback to simple hashing."""
        if self.use_ml and self.model:
            try:
                return self.model.encode(texts).tolist()
            except Exception as e:
                logger.error(f"ML encoding failed: {e}")
                return self._simple_encode(texts)
        else:
            return self._simple_encode(texts)
    
    def _simple_encode(self, texts: List[str]) -> List[List[float]]:
        """Simple fallback encoding using text hashing and basic features."""
        embeddings = []
        for text in texts:
            # Create a simple 384-dimensional vector based on text features
            embedding = [0.0] * 384
            
            # Basic text features
            text_lower = text.lower()
            text_hash = hashlib.md5(text.encode()).hexdigest()
            
            # Fill embedding with basic features
            for i, char in enumerate(text_hash[:32]):  # First 32 hex chars
                idx = int(char, 16) * 12  # Spread across 384 dimensions
                if idx < 384:
                    embedding[idx] = 1.0
            
            # Add length and word count features
            embedding[0] = min(len(text) / 1000.0, 1.0)  # Normalized length
            embedding[1] = min(len(text.split()) / 100.0, 1.0)  # Normalized word count
            
            # Add keyword-based features
            keywords = ['error', 'warning', 'info', 'debug', 'critical', 'exception', 'failed']
            for i, keyword in enumerate(keywords):
                if keyword in text_lower:
                    embedding[i + 2] = 1.0
            
            embeddings.append(embedding)
        
        return embeddings


# Singleton instance
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    """Get the global embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
