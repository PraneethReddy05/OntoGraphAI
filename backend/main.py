from .graph.graph_manager import GraphManager
from .agents.SeedAgent import SeedAgent
from .agents.CitationAgent import CitationAgent
from .agents.AuthorAgent import AuthorAgent
from .agents.ConceptAgent import ConceptAgent

# Setup
graph_manager = GraphManager()
seed_agent = SeedAgent(graph_manager)
citation_agent = CitationAgent(graph_manager)
concept_agent = ConceptAgent(graph_manager)

# Run agent on a topic
result = seed_agent.run("Bitcoin")
print(result)

# Run Citation Agent on the addend paper
res = citation_agent.run(result["paper"])
# Adding concepts for the seed paper
concept_result = concept_agent.run(result["paper"])

# Adding authors
author_agent = AuthorAgent(graph_manager)
for seed, paper_id in res["new_references"]:
    author_result = author_agent.run(paper_id)
    concept_result = concept_agent.run(paper_id)
    print(author_result)

# Visualize
graph_manager.visualize()
