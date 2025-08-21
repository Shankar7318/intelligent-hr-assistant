import re
import string
from typing import List

class TextPreprocessor:
    def __init__(self):
        pass
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        return text.split()
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove common stopwords"""
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'
        }
        return [token for token in tokens if token not in stopwords]
    
    def stem_words(self, tokens: List[str]) -> List[str]:
        """Simple stemming (placeholder for proper stemmer)"""
        # In a real implementation, you'd use nltk or similar
        stem_map = {
            'engineering': 'engineer',
            'developer': 'develop',
            'manager': 'manage',
            'analyst': 'analy',
            'designer': 'design'
        }
        
        return [stem_map.get(token, token) for token in tokens]
    
    def preprocess(self, text: str) -> List[str]:
        """Full preprocessing pipeline"""
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        filtered = self.remove_stopwords(tokens)
        stemmed = self.stem_words(filtered)
        return stemmed