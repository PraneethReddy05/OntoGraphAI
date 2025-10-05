# backend/agents/author_agent.py
import logging
from .BaseAgent import BaseAgent
from backend.services.openalex_service import OpenAlexService

class AuthorAgent(BaseAgent):
    """
    Adds author information for a given paper.
    """

    def __init__(self, graph_manager):
        super().__init__(name="AuthorAgent", graph_manager=graph_manager)
        self.openalex = OpenAlexService()
        logging.basicConfig(level=logging.INFO)
        self.paper = ""

    def perceive(self, paper_id):
        """
        Fetch paper details and extract authors.
        :param paper_id: str - OpenAlex paper ID
        :return: list of author dicts [{id, name}, ...]
        """
        logging.info(f"[{self.name}] Fetching authors for {paper_id}")
        paper_data = self.openalex.get_paper_by_id(paper_id)
        if not paper_data:
            logging.warning(f"[{self.name}] Paper {paper_id} not found.")
            return []

        self.paper = paper_data.get("title")
        authorships = paper_data.get("authorships", [])
        authors = []
        for a in authorships:
            author_info = a.get("author", {})
            if author_info:
                authors.append({
                    "id": author_info.get("id", None),
                    "name": author_info.get("display_name", "Unknown Author")
                })

        logging.info(f"[{self.name}] Found {len(authors)} authors.")
        return authors

    def decide(self, perception):
        """
        Decide which authors to add (skip duplicates).
        """
        if not perception:
            return None

        new_authors = []
        for author in perception:
            flag = True if not self.graph_manager.has_node(author["name"]) else False
            new_authors.append((author,flag))
        logging.info(f"[{self.name}] {len(new_authors)} new authors to add.")
        return new_authors

    def act(self, authors):
        """
        Add author nodes and connect them to the paper.
        """
        if not authors:
            return None

        # For simplicity, assume this agent runs on one paper at a time
        # paper_node = list(self.graph_manager.G.nodes)[-1]  # last added paper
        added_edges = []

        for author, flag in authors:
            if flag:
                self.graph_manager.add_node(author["name"], ntype="Author")
            self.graph_manager.add_edge(author["name"], self.paper, relation="writtenBy")
            added_edges.append((author["name"], self.paper))

        logging.info(f"[{self.name}] Added {len(added_edges)} writtenBy edges.")
        return {"authors_added": [a for a, _ in authors]}
