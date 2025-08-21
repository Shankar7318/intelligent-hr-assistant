from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ResumeParseRequest(BaseModel):
    file_path: str
    extract_skills: bool = True
    extract_experience: bool = True

class ResumeParseResponse(BaseModel):
    success: bool
    data: dict
    error: Optional[str] = None

class JobDescriptionRequest(BaseModel):
    role: str
    skills: List[str]
    experience_level: Optional[str] = None
    budget_range: Optional[str] = None

class JobDescriptionResponse(BaseModel):
    success: bool
    job_description: dict
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None