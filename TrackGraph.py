class TrackGraph:
    def __init__(self):
        # Initialize an empty graph. This one will be like a "meta graph" that holds all our songs
        self.graph = {}

    def add_node(self, node):
        """Add a node to the graph (song, artist, tag, etc.)."""
        if node not in self.graph: # Create empty node if we dont have it yet
            self.graph[node] = {}

    def add_edge(self, node1, node2, relationship):
        """
        Add a relationship (edge) between two nodes.
        - node1: The starting node (like a song)
        - node2: The connected node (like a tag or artist)
        - relationship: Type of relationship (like "is a tag of", "is by artist")
        """
        self.add_node(node1)
        self.add_node(node2)

        # Create relationship if we dont have it yet
        if relationship not in self.graph[node1]:
            self.graph[node1][relationship] = set()

        # Add node2 to the set of connected nodes for node1 with this relationship
        self.graph[node1][relationship].add(node2)

# Testing
track_graph = TrackGraph()

# Add nodes (songs, tags, artists)
track_graph.add_node("Emerald and Stone")
track_graph.add_node("ambient")
track_graph.add_node("Brian Eno")

# Add relationships (edges)
track_graph.add_edge("ambient", "Emerald and Stone", "is a tag of")
track_graph.add_edge("Emerald and Stone", "Brian Eno", "is by artist")
