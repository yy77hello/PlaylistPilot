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


    def get_connected_nodes(self, node, relationship):
        """
        Get all nodes connected to the given node by the specified relationship.
        - node: The node for which to find connected nodes
        - relationship: The relationship type to filter connections by
        """
        # Check if the node exists in the graph
        if node in self.graph:
            node_data = self.graph[node]  # Get the data associated with the node

            # Check if the relationship exists for the node
            if relationship in node_data: # Inside node data we have keys (our relationships) and the values are dictionaries of the items we are reffering to
                connected_nodes = node_data[relationship]  # Get the connected nodes for this relationship
                return connected_nodes  # Return the set of connected nodes
        else:
            # If the node doesn't exist in the graph or if the relationship doesnt exist, return an empty set
            return set()

    def get_all_relationships(self, node):
        """
        Get all relationships of a given node (tags, artists, etc.).
        - node: The node for which to get relationships
        """
        # Check if the node exists in the graph
        if node in self.graph:
            node_data = self.graph[node]  # Get the data associated with the node

            # Pull all relationships (as key-value pairs) for this node
            return node_data.items()
        else:
            # If the node doesn't exist in the graph we just return an empty list
            return []


# Testing
track_graph = TrackGraph()

# Add nodes (songs, tags, artists)
track_graph.add_node("Emerald and Stone")
track_graph.add_node("ambient")
track_graph.add_node("Brian Eno")

# Add relationships (edges)
track_graph.add_edge("ambient", "Emerald and Stone", "is a tag of")
track_graph.add_edge("Emerald and Stone", "Brian Eno", "is by artist")

# Accessing connected nodes:
# Get all songs tagged with 'ambient'
connected_songs = track_graph.get_connected_nodes("ambient", "is a tag of")
print(connected_songs)  # Output: {'song: Emerald and Stone'}

# Get all artists of the song 'Emerald and Stone'
connected_artists = track_graph.get_connected_nodes("Emerald and Stone", "is by artist")
print(connected_artists)  # Output: {'Brian Eno'}

# Get all relationships of a song
relationships = track_graph.get_all_relationships("Emerald and Stone")
for relationship, nodes in relationships:
    print(f"Relationship: {relationship}")
    print(f"Connected Nodes: {nodes}")
