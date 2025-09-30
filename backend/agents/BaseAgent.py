from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    Defines the core lifecycle: perceive -> decide -> act.
    """
    def __init__(self, name: str, graph_manager):
        """
        :param name: str - Name of the agent (e.g., 'SeedAgent')
        :param graph_manager: GraphManager - Handles interactions with the knowledge graph
        """
        self.name = name
        self.graph_manager = graph_manager
        self.memory = [] # internal memory for the agent(logs, past actions)
    
    @abstractmethod
    def perceive(self, input_data):
        """
        Observe the environment (graph state, API input, etc.)
        :param input_data: Contextual information (paper ID, topic, etc.)
        :return: processed input for decision-making
        """
        pass

    @abstractmethod
    def decide(self, perception):
        """
        Make a decision about what action to take.
        :param perception: Data returned by perceive()
        :return: action (could be a dict or string describing the task)
        """
        pass
    
    @abstractmethod
    def act(self, action):
        """
        Execute the decided action and update the graph.
        :param action: The chosen action from decide()
        :return: result of action (e.g., updated nodes/edges)
        """
        pass
    
    def run(self, input_data):
        """
        Run a full agent cycle: perceive -> decide -> act
        :param input_data: External input (e.g., paper ID, topic)
        """
        perception = self.perceive(input_data)
        decision = self.decide(perception)
        result = self.act(decision)
        self.memory.append({
            "input": input_data,
            "perception": perception,
            "decision": decision,
            "result": result
        })
        return result