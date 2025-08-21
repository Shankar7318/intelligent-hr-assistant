from fastapi import APIRouter, UploadFile, File, HTTPException
from src.data_processing.resume_parser import EnhancedResumeParser
from agents.jd_agent import JDAgent
from .models import *

router = APIRouter()
resume_parser = EnhancedResumeParser()
jd_agent = JDAgent()

@router.post("/parse-resume", response_model=ResumeParseResponse)
async def parse_resume(file: UploadFile = File(...)):
    """Parse a resume file"""
    try:
        # Save uploaded file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Parse resume
        result = resume_parser.parse_resume(file_path)
        return ResumeParseResponse(success=True, data=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-job-description", response_model=JobDescriptionResponse)
async def generate_job_description(request: JobDescriptionRequest):
    """Generate a job description"""
    try:
        state = {
            "current_role": request.role,
            "required_skills": request.skills,
            "experience_level": request.experience_level,
            "budget_range": request.budget_range,
            "company_info": {}
        }
        
        result = jd_agent.generate_jd(state)
        return JobDescriptionResponse(success=True, job_description=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(status="healthy", timestamp="2024-01-01T00:00:00Z")