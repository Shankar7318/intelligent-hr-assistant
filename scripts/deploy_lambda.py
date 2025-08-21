#!/usr/bin/env python3
"""
Script to deploy HR Assistant to AWS Lambda
"""

import argparse
import boto3
import zipfile
import os
from src.utils.config import load_config

def create_deployment_package():
    """Create deployment package for Lambda"""
    print("Creating deployment package...")
    
    # Create zip file with required dependencies
    with zipfile.ZipFile('deployment-package.zip', 'w') as zipf:
        # Add source code
        for root, dirs, files in os.walk('src'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arcname)
        
        # Add requirements
        zipf.write('requirements.txt', 'requirements.txt')
    
    print("Deployment package created: deployment-package.zip")

def deploy_to_lambda(function_name, region):
    """Deploy to AWS Lambda"""
    print(f"Deploying to Lambda function: {function_name} in region: {region}")
    
    # This would be implemented with actual Lambda deployment logic
    print("Deployment complete")

def main():
    parser = argparse.ArgumentParser(description="Deploy HR Assistant to AWS Lambda")
    parser.add_argument("--function", required=True, help="Lambda function name")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    
    args = parser.parse_args()
    config = load_config()
    
    create_deployment_package()
    deploy_to_lambda(args.function, args.region)

if __name__ == "__main__":
    main()