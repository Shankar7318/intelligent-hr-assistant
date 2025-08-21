from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embeddings"""
        return self.model.encode(texts)
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    
    def batch_similarity(self, query_embedding: np.ndarray, target_embeddings: np.ndarray) -> List[float]:
        """Calculate similarities between query and multiple targets"""
        similarities = []
        for target in target_embeddings:
            similarities.append(self.similarity(query_embedding, target))
        return similarities