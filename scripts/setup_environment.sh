#!/bin/bash

echo "🚀 Setting up Intelligent HR Assistant environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p data/raw_resumes data/processed_resumes data/job_descriptions
mkdir -p data/knowledge_graph data/user_data/user_profiles data/job_database
mkdir -p models logs tests deployment scripts

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "🔧 Downloading spaCy model..."
python -m spacy download en_core_web_lg

# Create default configuration files
echo "⚙️  Creating configuration files..."

# config.yaml
if [ ! -f config.yaml ]; then
    cat > config.yaml << 'EOL'
app:
  name: "Intelligent HR Assistant"
  version: "1.0.0"
  environment: "development"

llm:
  default_provider: "openai"
  model: "gpt-4-turbo-preview"
  temperature: 0.7
  max_tokens: 4000

database:
  type: "sqlite"
  path: "data/hr_assistant.db"
  echo: false

api:
  host: "0.0.0.0"
  port: 8000
  debug: false
  cors_origins: ["*"]

streamlit:
  host: "0.0.0.0"
  port: 8501
  theme: "light"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/app.log"

features:
  agentic_system: true
  resume_parsing: true
  job_matching: true
  application_tracking: true
  reminders: true
EOL
    echo "✅ Created config.yaml"
else
    echo "⚠️  config.yaml already exists, skipping..."
fi

# .env file
if [ ! -f .env ]; then
    cat > .env << 'EOL'
# API Keys (get these from respective providers)
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=sqlite:///data/hr_assistant.db

# Application
LOG_LEVEL=INFO
DEBUG=False
ENVIRONMENT=development

# Email (for reminders - optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EOL
    echo "✅ Created .env file"
    echo "⚠️  Please update .env file with your actual API keys"
else
    echo "⚠️  .env file already exists, skipping..."
fi

# Create __init__.py files for packages
echo "📦 Initializing Python packages..."
find . -name "__init__.py" -exec touch {} \; 2>/dev/null || true

# Set execute permissions on scripts
chmod +x scripts/*.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python run.py --web (for web interface)"
echo "4. Run: python run.py --cli (for CLI version)"
echo "5. Run: python run.py --api (for API server)"
echo ""
echo "For production:"
echo "- Update config.yaml for production environment"
echo "- Configure proper database (PostgreSQL recommended)"
echo "- Set up proper email configuration for reminders"