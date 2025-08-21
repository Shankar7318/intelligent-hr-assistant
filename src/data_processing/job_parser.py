import re
from typing import Dict, List, Any

class JobParser:
    def __init__(self):
        pass
    
    def parse_job_description(self, text: str) -> Dict[str, Any]:
        """Parse job description text into structured data"""
        return {
            "title": self.extract_title(text),
            "company": self.extract_company(text),
            "location": self.extract_location(text),
            "salary": self.extract_salary(text),
            "requirements": self.extract_requirements(text),
            "responsibilities": self.extract_responsibilities(text),
            "benefits": self.extract_benefits(text)
        }
    
    def extract_title(self, text: str) -> str:
        # Simple title extraction
        lines = text.split('\n')
        for line in lines:
            if line.strip() and len(line.strip()) < 100:
                return line.strip()
        return "Unknown Position"
    
    def extract_company(self, text: str) -> str:
        # Placeholder for company extraction
        return "Unknown Company"
    
    def extract_location(self, text: str) -> str:
        # Simple location pattern matching
        patterns = [
            r'\b(?:remote|hybrid|onsite)\b',
            r'\b[A-Z][a-z]+,\s*[A-Z]{2}\b',
            r'\b(?:san francisco|new york|los angeles|chicago|austin)\b'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return "Location not specified"
    
    def extract_salary(self, text: str) -> str:
        # Salary pattern matching
        patterns = [
            r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*-\s*\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
            r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:per year|annually|annual)',
            r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:per hour|hourly)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return "Salary not specified"
    
    def extract_requirements(self, text: str) -> List[str]:
        # Simple requirement extraction
        requirements = []
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['requirement', 'qualification', 'must have', 'should have']):
                requirements.append(line.strip())
        
        return requirements
    
    def extract_responsibilities(self, text: str) -> List[str]:
        # Simple responsibility extraction
        responsibilities = []
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['responsibility', 'duty', 'role', 'will']):
                responsibilities.append(line.strip())
        
        return responsibilities
    
    def extract_benefits(self, text: str) -> List[str]:
        # Simple benefits extraction
        benefits = []
        lines = text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['benefit', 'perk', 'advantage', 'offer']):
                benefits.append(line.strip())
        
        return benefits