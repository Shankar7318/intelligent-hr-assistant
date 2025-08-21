import boto3
from src.utils.config import load_config

class AWSUtils:
    def __init__(self):
        self.config = load_config()
        self.session = boto3.Session()
    
    def get_s3_client(self):
        """Get S3 client"""
        return self.session.client('s3')
    
    def upload_file(self, file_path, bucket_name, object_name):
        """Upload file to S3"""
        s3_client = self.get_s3_client()
        try:
            s3_client.upload_file(file_path, bucket_name, object_name)
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False