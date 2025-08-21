# 🤖 Intelligent HR Assistant

A comprehensive AI-powered HR assistant that streamlines hiring processes with multi-agent systems, resume parsing, job matching, and automated workflows.

## Features

- **🤖 Multi-Agent System**: AI agents for JD generation, checklist creation, and resume analysis
- **📝 Resume Parsing**: Advanced NLP-based resume analysis and extraction
- **🔍 Job Matching**: Intelligent candidate-job matching with similarity scoring
- **📊 Application Tracking**: Complete job application management system
- **⏰ Smart Reminders**: Automated follow-up and reminder system
- **🌐 Web Interface**: Streamlit-based user-friendly interface
- **🔌 API Support**: RESTful API for integration with other systems
- **🐳 Docker Ready**: Containerized deployment with Docker

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Virtual environment recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shankar7318/intelligent-hr-assistant.git
   cd intelligent-hr-assistant
2. **Run setup script**
   ```bash
   chmod +x scripts/setup_environment.sh
   ./scripts/setup_environment.sh
3. **Configure API keys**
   ```bash
   #Edit .env file with your actual API keys
   nano .env
4. **Activate virtual environment**
  ``` bash
   source venv/bin/activate

5.**Run the application**
   ```bash
# Web interface (default)
python run.py --web

# CLI version
python run.py --cli

# API server
python run.py --api

```bash
Usage
Web Interface
Access the web interface at http://localhost:8501

API Endpoints
GET /health - Health check

POST /parse-resume - Parse resume file

POST /generate-jd - Generate job description

POST /match-candidate - Match candidate to jobs
CLI Mode
Run python run.py --cli for command-line interaction
```bash

```bash
Project Structure:
intelligent-hr-assistant/
├── agents/          # AI agents
├── graph/           # LangGraph state management
├── src/            # Core functionality
├── streamlit_app/  # Web interface
├── data/           # Data storage
├── tests/          # Test suite
└── deployment/     # Deployment config

Configuration
Edit config.yaml for application settings and .env for environment variables.
```bash

### Deployment
#Docker
```bash
docker build -t hr-assistant .
docker run -p 8501:8501 -p 8000:8000 hr-assistant

#Docker Compose
docker-compose up -d


#Running Tests 
python -m pytest tests/
#code formatting
black .
isort .
```bash

