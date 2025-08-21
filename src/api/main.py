from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as api_router
from src.utils.config import load_config

def create_app():
    """Create FastAPI application"""
    config = load_config()
    
    app = FastAPI(
        title="Intelligent HR Assistant API",
        description="API for AI-powered HR assistant",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config['api']['cors_origins'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    return app

app = create_app()

@app.get("/")
async def root():
    return {"message": "Intelligent HR Assistant API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}