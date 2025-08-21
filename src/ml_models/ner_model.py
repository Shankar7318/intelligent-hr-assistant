import spacy
from typing import List, Dict, Any

class NERModel:
    def __init__(self, model_name="en_core_web_lg"):
        self.nlp = spacy.load(model_name)
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from text"""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        
        return entities
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using pattern matching"""
        skills = []
        skill_patterns = [
            r'\b(?:python|java|javascript|typescript|react|angular|vue)\b',
            r'\b(?:machine learning|deep learning|ai|nlp|computer vision)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|terraform)\b',
            r'\b(?:sql|mysql|postgresql|mongodb|redis)\b'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)
        
        return list(set(skills))