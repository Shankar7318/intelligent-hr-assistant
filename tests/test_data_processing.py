import unittest
from src.data_processing.resume_parser import EnhancedResumeParser
from src.data_processing.job_parser import JobParser

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.resume_parser = EnhancedResumeParser()
        self.job_parser = JobParser()
    
    def test_resume_parser_initialization(self):
        self.assertIsNotNone(self.resume_parser)
    
    def test_job_parser_initialization(self):
        self.assertIsNotNone(self.job_parser)
    
    def test_text_extraction(self):
        # Test with sample text
        sample_text = "John Doe\nSoftware Engineer\nPython, Java, AWS"
        skills = self.resume_parser.extract_skills(sample_text)
        self.assertIn("python", [s.lower() for s in skills.get("programming", [])])

if __name__ == "__main__":
    unittest.main()