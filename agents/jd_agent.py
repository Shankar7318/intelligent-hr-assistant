from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from stateclass import JobDescription
from llm_init import primary_llm

class JDAgent:
    def __init__(self):
        self.llm = primary_llm
        self.parser = PydanticOutputParser(pydantic_object=JobDescription)
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an expert HR professional and job description writer. 
            Create a comprehensive job description based on the following requirements:
            
            Role: {role}
            Required Skills: {skills}
            Experience Level: {experience}
            Budget Range: {budget}
            Company Info: {company_info}
            
            {format_instructions}
            
            Make the job description compelling, inclusive, and optimized for attracting top talent.
            Include competitive benefits and a clear application process.
            """
        )
        
        self.chain = self.prompt | self.llm | self.parser
        
    def generate_jd(self, state):
        """Generate a job description based on the current state"""
        if not all([state.get('current_role'), state.get('required_skills')]):
            return {"messages": [{"type": "ai", "content": "I need more information about the role and required skills to generate a job description."}]}
        
        try:
            jd = self.chain.invoke({
                "role": state['current_role'],
                "skills": ", ".join(state['required_skills']),
                "experience": state.get('experience_level', 'Not specified'),
                "budget": state.get('budget_range', 'Not specified'),
                "company_info": str(state.get('company_info', {})),
                "format_instructions": self.parser.get_format_instructions()
            })
            
            jd_markdown = self._format_jd_to_markdown(jd)
            return {
                "messages": [{"type": "ai", "content": jd_markdown}],
                "jd_generated": True
            }
            
        except Exception as e:
            return {"messages": [{"type": "ai", "content": f"Error generating job description: {str(e)}"}]}
    
    def _format_jd_to_markdown(self, jd: JobDescription) -> str:
        """Convert JobDescription object to markdown format"""
        markdown = f"# {jd.title}\n\n"
        markdown += f"**Department:** {jd.department} | **Location:** {jd.location} | **Type:** {jd.job_type}\n\n"
        markdown += f"**Salary Range:** {jd.salary_range}\n\n"
        
        markdown += "## Job Summary\n"
        markdown += f"{jd.summary}\n\n"
        
        markdown += "## Key Responsibilities\n"
        for responsibility in jd.responsibilities:
            markdown += f"- {responsibility}\n"
        markdown += "\n"
        
        markdown += "## Requirements\n"
        for requirement in jd.requirements:
            markdown += f"- {requirement}\n"
        markdown += "\n"
        
        if jd.preferred_qualifications:
            markdown += "## Preferred Qualifications\n"
            for qualification in jd.preferred_qualifications:
                markdown += f"- {qualification}\n"
            markdown += "\n"
        
        if jd.benefits:
            markdown += "## Benefits\n"
            for benefit in jd.benefits:
                markdown += f"- {benefit}\n"
            markdown += "\n"
        
        markdown += "## Application Process\n"
        markdown += f"{jd.application_process}\n"
        
        return markdown