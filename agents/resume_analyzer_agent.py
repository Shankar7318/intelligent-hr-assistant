from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_init import primary_llm

class ResumeAnalyzerAgent:
    def __init__(self):
        self.llm = primary_llm
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            Analyze the following resume content and provide a comprehensive assessment:
            
            {resume_text}
            
            Please provide analysis in the following format:
            
            ## Summary
            [Overall summary of the candidate]
            
            ## Skills Assessment
            - Technical Skills: [list and assessment]
            - Soft Skills: [list and assessment]
            
            ## Experience Level
            [Years and quality of experience]
            
            ## Education
            [Educational background assessment]
            
            ## Potential Roles
            [Suggested roles this candidate would be good for]
            
            ## Recommendations
            [Hiring recommendations and next steps]
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def analyze_resume(self, resume_text):
        """Analyze resume content and provide assessment"""
        try:
            analysis = self.chain.invoke({"resume_text": resume_text})
            return {
                "success": True,
                "analysis": analysis,
                "messages": [{"type": "ai", "content": analysis}]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "messages": [{"type": "ai", "content": f"Error analyzing resume: {str(e)}"}]
            }