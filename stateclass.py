from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from datetime import datetime

class AgentState(TypedDict):
    messages: List[BaseMessage]
    current_role: Optional[str]
    required_skills: List[str]
    experience_level: Optional[str]
    budget_range: Optional[str]
    hiring_timeline: Optional[str]
    company_info: Dict[str, Any]
    jd_generated: bool
    checklist_generated: bool
    current_agent: Optional[str]
    user_id: Optional[str]
    session_id: Optional[str]

class HiringChecklist(BaseModel):
    steps: List[Dict[str, Any]]
    estimated_timeline: str
    resources_needed: List[str]
    success_metrics: List[str]
    role: str
    created_at: datetime

class JobDescription(BaseModel):
    title: str
    department: str
    location: str
    job_type: str
    salary_range: str
    summary: str
    responsibilities: List[str]
    requirements: List[str]
    preferred_qualifications: List[str]
    benefits: List[str]
    application_process: str
    created_at: datetime

class JobApplication(BaseModel):
    id: int
    user_id: str
    job_id: str
    job_title: str
    company: str
    application_date: datetime
    status: str
    resume_match: float
    next_followup: Optional[datetime]
    history: List[Dict[str, Any]]

class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    current_title: Optional[str]
    experience: int
    skills: List[str]
    education: str
    resume_path: Optional[str]
    created_at: datetime
    updated_at: datetime