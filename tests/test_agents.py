import unittest
from agents.jd_agent import JDAgent
from agents.checklist_agent import ChecklistAgent

class TestAgents(unittest.TestCase):
    def setUp(self):
        self.jd_agent = JDAgent()
        self.checklist_agent = ChecklistAgent()
    
    def test_jd_agent_initialization(self):
        self.assertIsNotNone(self.jd_agent)
    
    def test_checklist_agent_initialization(self):
        self.assertIsNotNone(self.checklist_agent)
    
    def test_jd_generation(self):
        state = {
            "current_role": "Software Engineer",
            "required_skills": ["Python", "AWS"],
            "experience_level": "Mid-level",
            "budget_range": "$80,000 - $120,000"
        }
        
        result = self.jd_agent.generate_jd(state)
        self.assertIn("messages", result)

if __name__ == "__main__":
    unittest.main()