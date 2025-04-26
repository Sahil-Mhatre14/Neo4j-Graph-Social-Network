from py2neo import Graph

# Set your Neo4j credentials here
graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456789"))
