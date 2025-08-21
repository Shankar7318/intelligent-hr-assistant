#!/usr/bin/env python3
"""
Intelligent HR Assistant - Main Entry Point
"""

import argparse
import asyncio
from graph.stategraph import HRAssistantGraph
from stateclass import AgentState
from langchain_core.messages import HumanMessage
from src.utils.logger import setup_logging
from src.utils.config import load_config

def main():
    """Main CLI application"""
    parser = argparse.ArgumentParser(description="Intelligent HR Assistant")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--api", action="store_true", help="Start API server")
    parser.add_argument("--web", action="store_true", help="Start web interface")
    parser.add_argument("--train", action="store_true", help="Train models")
    
    args = parser.parse_args()
    config = load_config()
    setup_logging(config)
    
    if args.cli:
        run_cli()
    elif args.api:
        run_api()
    elif args.web:
        run_web()
    elif args.train:
        train_models()
    else:
        run_web()

def run_cli():
    """Run the CLI version"""
    print("🤖 Intelligent HR Assistant - CLI Version")
    print("Type 'quit' to exit, 'reset' to start over\n")
    
    assistant = HRAssistantGraph()
    state = AgentState(
        messages=[],
        current_role=None,
        required_skills=[],
        experience_level=None,
        budget_range=None,
        hiring_timeline=None,
        company_info={},
        jd_generated=False,
        checklist_generated=False,
        current_agent=None
    )
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'reset':
                state = AgentState(
                    messages=[],
                    current_role=None,
                    required_skills=[],
                    experience_level=None,
                    budget_range=None,
                    hiring_timeline=None,
                    company_info=state.get('company_info', {}),
                    jd_generated=False,
                    checklist_generated=False,
                    current_agent=None
                )
                print("Conversation reset.")
                continue
            
            state['messages'].append(HumanMessage(content=user_input))
            new_state = assistant.invoke(state)
            state.update(new_state)
            
            ai_messages = [msg for msg in state['messages'] if hasattr(msg, 'type') and msg.type == 'ai']
            if ai_messages:
                print(f"Assistant: {ai_messages[-1].content}\n")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

def run_api():
    """Start the FastAPI server"""
    import uvicorn
    from src.api.main import app
    
    config = load_config()
    uvicorn.run(
        app,
        host=config['api']['host'],
        port=config['api']['port'],
        reload=config['api']['debug']
    )

def run_web():
    """Start the Streamlit web interface"""
    import subprocess
    import sys
    
    config = load_config()
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app/app.py",
        "--server.port", str(config['streamlit']['port']),
        "--server.address", config['streamlit']['host']
    ])

def train_models():
    """Train ML models"""
    from scripts.train_models import main as train_main
    train_main()

if __name__ == "__main__":
    main()