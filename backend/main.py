from .graph.graph_manager import GraphManager
from .agents.SeedAgent import SeedAgent
from .agents.CitationAgent import CitationAgent

# Setup
graph_manager = GraphManager()
seed_agent = SeedAgent(graph_manager)
citation_agent = CitationAgent(graph_manager)

# Run agent on a topic
result = seed_agent.run("Bitcoin")
print(result)

# Run Citation Agent on the addend paper
res = citation_agent.run(result["paper"])
print(res)

# Visualize
graph_manager.visualize()
