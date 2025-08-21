from langchain.tools import Tool
from typing import List, Dict, Any

class FunctionCallingHandler:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name: str, func: callable, description: str):
        """Register a function as a tool"""
        self.tools[name] = Tool(name=name, func=func, description=description)
    
    def get_tools(self) -> List[Tool]:
        """Get all registered tools"""
        return list(self.tools.values())
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        return self.tools[tool_name].func(**kwargs)
    
    def get_tool_descriptions(self) -> List[Dict[str, str]]:
        """Get descriptions of all tools"""
        return [{"name": name, "description": tool.description} for name, tool in self.tools.items()]