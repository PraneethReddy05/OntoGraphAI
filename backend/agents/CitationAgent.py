import logging
from .BaseAgent import BaseAgent
from ..services.openalex_service import OpenAlexService

class CitationAgent(BaseAgent):
    """
    Expands the graph by fetching references (citations) for a given paper node.
    """
    def __init__(self, graph_manager, max_refs = 5):
        super().__init__(name="CitationAgent", graph_manager=graph_manager)
        self.openalex = OpenAlexService()  # API wrapper
        self.max_citations = max_refs # Limit number of citations to add per paper
        logging.basicConfig(level=logging.INFO)

    def perceive(self, paper_id):
        """
        Fetch paper details from OpenAlex and extract referenced works.
        :param paper_id: str - OpenAlex ID (e.g., 'W2741809807')
        :return: list of referenced paper IDs
        """
        logging.info(f"{self.name} fetching references for {paper_id}")
        paper_data = self.openalex.get_paper_by_id(paper_id)
        if not paper_data:
            logging.warning(f"{self.name} No data found for paper ID: {paper_id}")
            return []
        refs = paper_data.get("referenced_works", [])
        logging.info(f"{self.name} found {len(refs)} references")
        return refs[:self.max_citations] # limit to max_refs
    
    def decide(self, perception):
        """
        Decide which references to add to the graph.
        Simple strategy: add all (up to max_refs).
        (stratrgy to be changed later)
        """

        if not perception:
            return None
        return perception

    def act(self, action):
        """
        Add the referenced papers to the graph and connect them.
        :param references: list of OpenAlex paper IDs
        """
        if not action:
            return None
        
        added_nodes = []
        for ref_id in action:
            ref_data = self.openalex.get_paper_by_id(ref_id)
            if not ref_data:
                continue

            title = ref_data.get("title", "Untitled Paper")
            self.graph_manager.add_node(title, ntype="Paper", title=title)

            # Create cites edges (original paper -> cited paper)
            citing_paper = list(self.graph_manager.G.nodes)[0]
            self.graph_manager.add_edge(citing_paper, title, relation="cites")
            added_nodes.append((citing_paper, title))

        logging.info(f"{self.name} Added {len(added_nodes)} citation edges.")
        return {"new_references": added_nodes}