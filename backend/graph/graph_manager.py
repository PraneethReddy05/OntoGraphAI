import networkx as nx
import matplotlib.pyplot as plt

class GraphManager:
    """
    Manages the knowledge graph. 
    Provides methods for adding nodes, edges, and visualization.
    Currently uses NetworkX, but can be extended to Neo4j.
    """
    def __init__(self):
        self.G = nx.DiGraph() # Directed graph (papers cite to other papers)

    def add_node(self, node_id, ntype="Entity", **attrs):
        """
        Add a node with attributes.
        :param node_id: Unique identifier (e.g., paper ID, author name)
        :param ntype: Node type ('Paper', 'Author', 'Concept')
        :param attrs: Additional metadata (title, year, etc.)
        """
        if node_id not in self.G.nodes:
            self.G.add_node(node_id, type=ntype, **attrs)

    def get_node(self, node_id):
        return self.G.nodes[node_id] if node_id in self.G.nodes else None

    def has_node(self, node_id):
        return node_id in self.G.nodes

    # ------------------ Edge Management ------------------
    def add_edge(self, source, target, relation):
        """
        Add a directed edge with a relation label.
        Example: author -> paper [relation=writtenBy]
        """
        self.G.add_edge(source, target, relation=relation)

    def has_edge(self, source, target):
        return self.G.has_edge(source, target)

    def get_neighbors(self, node_id):
        return list(self.G.neighbors(node_id))

    # ------------------ Graph Visualization ------------------
    def visualize(self, figsize=(10, 8)):
        """
        Visualize the graph with node types and relation labels.
        """
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, seed=42)

        # Color nodes by type
        color_map = []
        for node in self.G.nodes(data=True):
            ntype = node[1].get("type", "Entity")
            if ntype == "Paper":
                color_map.append("lightblue")
            elif ntype == "Author":
                color_map.append("lightgreen")
            elif ntype == "Concept":
                color_map.append("orange")
            else:
                color_map.append("grey")

        nx.draw(
            self.G, pos, with_labels=True, node_color=color_map, 
            node_size=2000, font_size=9, font_weight="bold", edgecolors="black"
        )

        edge_labels = nx.get_edge_attributes(self.G, "relation")
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=8)
        plt.show()

    # ------------------ Export ------------------
    def export_graph(self, path="data/exports/graph.json"):
        """
        Export graph as JSON-like structure for frontend/analysis.
        """
        data = nx.node_link_data(self.G)
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return path

    def import_graph(self, path):
        """
        Load graph from exported JSON.
        """
        import json
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.G = nx.node_link_graph(data) 