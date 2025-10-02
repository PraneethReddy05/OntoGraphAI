import logging
from .BaseAgent import BaseAgent
from backend.services.openalex_service import OpenAlexService

class SeedAgent(BaseAgent):
    """
    The SeedAgent initializes the knowledge graph with a starting paper or topic.
    """
    def __init__(self, graph_manager):
        super().__init__(name= "SeedAgent", graph_manager=graph_manager)
        self.openalex = OpenAlexService() #API wrapper 

    def perceive(self, input_data):
        """
        Input can be:
        - DOI (e.g., '10.1038/s41586-020-2649-2')
        - OpenAlex ID (e.g., 'W2741809807')
        - Search topic (string, e.g., 'Knowledge Graphs')
        """
        logging.info(f"{self.name} Perceiving input: {input_data}")
        if input_data.startswith("10."): #DOI
            return self.openalex.get_paper_by_doi(input_data)
        elif input_data.startswith("W"): #OpenAlex Work ID
            return self.openalex.get_paper_by_id(input_data)
        else: #Treat as topic search
            return self.openalex.search_papers_by_topic(input_data, limit=1)

    def decide(self, perception):
        """
        Decide which paper(s) to add as seeds.
        For simplicity: take the first valid paper.
        """
        if not perception:
            logging.warning(f"{self.name} No valid perception data.")
            return None 

        # Normalize into a single paper dict
        if isinstance(perception, list):
            return perception[0] # first paper
        return perception # already a single paper dict
    
    def act(self, action):
        """
        Insert the chosen seed paper into the graph.
        """
        if not action:
            logging.warning(f"{self.name} No action to perform.")
            return None
        
        paper_id = action.get("id", "Unknown")
        title = action.get("title", "Untitled Paper")
        authors = [a["author"]["display_name"] for a in action.get("authorships", [])]

        # Add paper node
        self.graph_manager.add_node(paper_id, ntype="Paper", title = title)

        # Add author nodes + edges
        for author in authors:
            self.graph_manager.add_node(author, ntype="Author")
            self.graph_manager.add_edge(author, paper_id, relation="writtenBy")
        
        logging.info(f"{self.name} Added seed paper '{title}' with {len(authors)} authors.")
        return {"paper": paper_id, "title": title, "authors": authors}