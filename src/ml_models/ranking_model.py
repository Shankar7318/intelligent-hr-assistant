from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any

class RankingModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
    
    def fit(self, documents: List[str]):
        """Fit the vectorizer on documents"""
        self.vectorizer.fit(documents)
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """Transform texts to TF-IDF vectors"""
        return self.vectorizer.transform(texts).toarray()
    
    def rank_documents(self, query: str, documents: List[str]) -> List[Dict[str, Any]]:
        """Rank documents by relevance to query"""
        # Add query to documents for transformation
        all_texts = [query] + documents
        vectors = self.transform(all_texts)
        
        # Calculate similarities
        query_vector = vectors[0]
        doc_vectors = vectors[1:]
        
        similarities = cosine_similarity([query_vector], doc_vectors)[0]
        
        # Create ranked results
        results = []
        for i, (doc, similarity) in enumerate(zip(documents, similarities)):
            results.append({
                "rank": i + 1,
                "document": doc,
                "similarity": float(similarity),
                "score": float(similarity * 100)
            })
        
        # Sort by similarity descending
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        return results