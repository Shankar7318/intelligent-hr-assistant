from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from llm_init import primary_llm

class QueryProcessor:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.chain = ConversationChain(
            llm=primary_llm,
            memory=self.memory,
            verbose=True
        )
    
    def process_query(self, query: str) -> str:
        """Process a user query with conversation memory"""
        return self.chain.run(query)
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()