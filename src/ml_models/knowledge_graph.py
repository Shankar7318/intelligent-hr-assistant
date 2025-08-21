import networkx as nx
from typing import Dict, List, Any

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.Graph()
    
    def add_entity(self, entity_id: str, properties: Dict[str, Any]):
        """Add an entity to the knowledge graph"""
        self.graph.add_node(entity_id, **properties)
    
    def add_relation(self, source_id: str, target_id: str, relation_type: str, properties: Dict[str, Any] = None):
        """Add a relation between entities"""
        if properties is None:
            properties = {}
        self.graph.add_edge(source_id, target_id, relation=relation_type, **properties)
    
    def query_entities(self, properties: Dict[str, Any]) -> List[str]:
        """Query entities by properties"""
        results = []
        for node, data in self.graph.nodes(data=True):
            if all(data.get(key) == value for key, value in properties.items()):
                results.append(node)
        return results
    
    def get_relations(self, entity_id: str) -> List[Dict[str, Any]]:
        """Get all relations for an entity"""
        relations = []
        for neighbor in self.graph.neighbors(entity_id):
            edge_data = self.graph[entity_id][neighbor]
            relations.append({
                "target": neighbor,
                "relation": edge_data.get("relation", "unknown"),
                "properties": {k: v for k, v in edge_data.items() if k != "relation"}
            })
        return relations
    
    def find_paths(self, source_id: str, target_id: str, max_paths: int = 3) -> List[List[str]]:
        """Find paths between entities"""
        try:
            paths = list(nx.all_simple_paths(self.graph, source_id, target_id, cutoff=3))
            return paths[:max_paths]
        except:
            return []