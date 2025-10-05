# backend/agents/concept_agent.py
import logging
from .BaseAgent import BaseAgent
from backend.services.openalex_service import OpenAlexService

class ConceptAgent(BaseAgent):
    """
    Enriches papers with associated research concepts (topics/fields).
    """

    def __init__(self, graph_manager, max_concepts=5):
        super().__init__(name="ConceptAgent", graph_manager=graph_manager)
        self.openalex = OpenAlexService()
        self.max_concepts = max_concepts
        self.paper = ""
        logging.basicConfig(level=logging.INFO)

    def perceive(self, paper_id):
        """
        Fetch paper concepts from OpenAlex.
        :param paper_id: str - OpenAlex paper ID
        :return: list of concept dicts [{id, name, level, score}, ...]
        """
        logging.info(f"[{self.name}] Fetching concepts for {paper_id}")
        paper_data = self.openalex.get_paper_by_id(paper_id)
        self.paper = paper_data.get("title", "")
        if not paper_data:
            logging.warning(f"[{self.name}] Paper {paper_id} not found.")
            return []

        concepts = paper_data.get("concepts", [])
        concepts_list = []
        for c in concepts:
            if c.get("score", 0) > 0.5: # Threshold to filter relevant concepts
                concepts_list.append({
                    "id": c.get("id"),
                    "name": c.get("display_name"),
                    "level": c.get("level"),
                    "score": c.get("score")
                })
        logging.info(f"[{self.name}] Found {len(concepts_list)} concepts.")
        return concepts_list[:self.max_concepts]

    def decide(self, perception):
        """
        Decide which new concepts to add to the graph (avoid duplicates).
        """
        if not perception:
            return None

        new_concepts = []
        for c in perception:
            flag = True if not self.graph_manager.has_node(c["name"]) else False
            # if not self.graph_manager.has_node(c["name"]):
            #     new_concepts.append(c)
            new_concepts.append((c,flag))

        logging.info(f"[{self.name}] {len(new_concepts)} new concepts to add.")
        return new_concepts

    def act(self, concepts):
        """
        Add concept nodes and link them to the paper via hasConcept.
        """
        if not concepts:
            return None

        # Assume this agent runs for one paper at a time
        # paper_node = list(self.graph_manager.G.nodes)[-1]
        added_edges = []
        for c, flag in concepts:
            if flag:
                self.graph_manager.add_node(c["name"], ntype="Concept", level=c.get("level"))
            self.graph_manager.add_edge(self.paper, c["name"], relation="hasConcept")
            added_edges.append((self.paper, c["name"]))

        logging.info(f"[{self.name}] Added {len(added_edges)} hasConcept edges.")
        return {"concepts_added": [c["name"] for c, _ in concepts]}
