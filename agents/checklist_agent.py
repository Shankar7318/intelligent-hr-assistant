from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from stateclass import HiringChecklist
from llm_init import primary_llm
from datetime import datetime

class ChecklistAgent:
    def __init__(self):
        self.llm = primary_llm
        self.parser = PydanticOutputParser(pydantic_object=HiringChecklist)
        
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an expert HR hiring specialist. Create a comprehensive hiring checklist 
            for the following role:
            
            Role: {role}
            Required Skills: {skills}
            Experience Level: {experience}
            Hiring Timeline: {timeline}
            Company Info: {company_info}
            
            {format_instructions}
            
            Include all stages from job posting to onboarding. Provide realistic timelines
            and identify key resources needed at each stage. Focus on best practices for
            attracting and evaluating diverse candidates.
            """
        )
        
        self.chain = self.prompt | self.llm | self.parser
        
    def generate_checklist(self, state):
        """Generate a hiring checklist based on the current state"""
        if not state.get('current_role'):
            return {"messages": [{"type": "ai", "content": "I need to know what role you're hiring for to create a checklist."}]}
        
        try:
            checklist = self.chain.invoke({
                "role": state['current_role'],
                "skills": ", ".join(state.get('required_skills', [])),
                "experience": state.get('experience_level', 'Not specified'),
                "timeline": state.get('hiring_timeline', 'Not specified'),
                "company_info": str(state.get('company_info', {})),
                "format_instructions": self.parser.get_format_instructions()
            })
            
            checklist.created_at = datetime.now()
            checklist.role = state['current_role']
            
            checklist_markdown = self._format_checklist_to_markdown(checklist)
            return {
                "messages": [{"type": "ai", "content": checklist_markdown}],
                "checklist_generated": True
            }
            
        except Exception as e:
            return {"messages": [{"type": "ai", "content": f"Error generating hiring checklist: {str(e)}"}]}
    
    def _format_checklist_to_markdown(self, checklist: HiringChecklist) -> str:
        """Convert HiringChecklist object to markdown format"""
        markdown = f"# Hiring Process Checklist for {checklist.role}\n\n"
        markdown += f"**Estimated Timeline:** {checklist.estimated_timeline}\n\n"
        
        markdown += "## Process Steps\n"
        for i, step in enumerate(checklist.steps, 1):
            markdown += f"{i}. **{step['name']}** - {step.get('description', '')}\n"
            if 'timeline' in step:
                markdown += f"   - Timeline: {step['timeline']}\n"
            if 'owner' in step:
                markdown += f"   - Owner: {step['owner']}\n"
            markdown += "\n"
        
        if checklist.resources_needed:
            markdown += "## Resources Needed\n"
            for resource in checklist.resources_needed:
                markdown += f"- {resource}\n"
            markdown += "\n"
        
        if checklist.success_metrics:
            markdown += "## Success Metrics\n"
            for metric in checklist.success_metrics:
                markdown += f"- {metric}\n"
        
        markdown += f"\n*Generated on {checklist.created_at.strftime('%Y-%m-%d %H:%M')}*"
        
        return markdown