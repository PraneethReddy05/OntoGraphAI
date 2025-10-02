from backend.graph.graph_manager import GraphManager
from backend.agents.SeedAgent import SeedAgent

# Setup
graph_manager = GraphManager()
agent = SeedAgent(graph_manager)

# Run agent on a topic
result = agent.run("Knowledge Graphs")
print(result)

# Visualize
graph_manager.visualize()
