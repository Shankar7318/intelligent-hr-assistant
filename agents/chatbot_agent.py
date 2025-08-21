from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_init import primary_llm
import re

class ChatbotAgent:
    def __init__(self):
        self.llm = primary_llm
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an AI HR assistant that helps with hiring processes. Your role is to:
            1. Ask clarifying questions about the role, required skills, experience level, budget, and timeline
            2. Route requests to appropriate specialized agents (JD writer, checklist generator)
            3. Provide helpful guidance about hiring best practices
            
            Be professional, engaging, and focused on gathering complete information before
            generating outputs. Always confirm you have all needed information before proceeding.
            """),
            ("human", "{input}"),
            ("ai", "{response}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def process_input(self, state, user_input):
        """Process user input and determine next action"""
        messages = state.get('messages', [])
        messages.append({"type": "human", "content": user_input})
        
        if self._should_generate_jd(state):
            return {
                "messages": messages,
                "current_agent": "jd_agent"
            }
        elif self._should_generate_checklist(state):
            return {
                "messages": messages,
                "current_agent": "checklist_agent"
            }
        else:
            response = self.chain.invoke({
                "input": user_input,
                "response": self._get_conversation_context(state)
            })
            
            messages.append({"type": "ai", "content": response})
            return {"messages": messages}
    
    def _should_generate_jd(self, state):
        """Check if we have enough information to generate a JD"""
        return (state.get('current_role') and 
                state.get('required_skills') and
                not state.get('jd_generated', False) and
                self._contains_jd_keywords(state.get('messages', [])))
    
    def _should_generate_checklist(self, state):
        """Check if we have enough information to generate a checklist"""
        return (state.get('current_role') and 
                not state.get('checklist_generated', False) and
                self._contains_checklist_keywords(state.get('messages', [])))
    
    def _contains_jd_keywords(self, messages):
        """Check if conversation contains JD-related keywords"""
        recent_text = " ".join([msg['content'] for msg in messages[-3:] if msg['type'] == 'human'])
        keywords = ['job description', 'jd', 'posting', 'description', 'write a job']
        return any(keyword in recent_text.lower() for keyword in keywords)
    
    def _contains_checklist_keywords(self, messages):
        """Check if conversation contains checklist-related keywords"""
        recent_text = " ".join([msg['content'] for msg in messages[-3:] if msg['type'] == 'human'])
        keywords = ['checklist', 'process', 'hiring plan', 'steps', 'timeline']
        return any(keyword in recent_text.lower() for keyword in keywords)
    
    def _get_conversation_context(self, state):
        """Extract relevant context from conversation"""
        context = "Conversation so far:\n"
        
        if state.get('current_role'):
            context += f"- Role: {state['current_role']}\n"
        if state.get('required_skills'):
            context += f"- Required Skills: {', '.join(state['required_skills'])}\n"
        if state.get('experience_level'):
            context += f"- Experience Level: {state['experience_level']}\n"
        if state.get('budget_range'):
            context += f"- Budget: {state['budget_range']}\n"
        if state.get('hiring_timeline'):
            context += f"- Timeline: {state['hiring_timeline']}\n"
        
        return context