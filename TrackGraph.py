from collections import defaultdict

class TrackGraph:
    def __init__(self):
        # Initialize an empty graph. This one will be like a "meta graph" that holds all our songs
        # Also initialize a dictionary for keeping track of how many times a tag is used.
        self.graph = {}
        self.tag_usage = defaultdict(int)

    def add_node(self, node):
        """Add a node to the graph (song, artist, tag, etc.)."""
        if node not in self.graph: # Create empty node if we dont have it yet
            self.graph[node] = {}

    def add_edge(self, node1, node2, relationship):
        """
        Add a relationship (edge) between two nodes, creating a two-way link
        for common relationships like 'has_tag'/'is_tag_of' and 'is_by_artist'/'has_track'.
        - node1: The starting node.
        - node2: The connected node.
        - relationship: The type of relationship.
        """
        self.add_node(node1)
        self.add_node(node2)

        # Create relationship if we dont have it yet
        if relationship not in self.graph[node1]:
            self.graph[node1][relationship] = set()

        is_new = node2 not in self.graph[node1][relationship]
        self.graph[node1][relationship].add(node2)

        # Add the reverse connection from node2 to node1 directly
        # We wanna have the relationship go the other way too because otherwise the tagging isnt gonna work when we run algorithms
        if relationship == "has_tag":
            reverse_relationship = "is_tag_of"
            if reverse_relationship not in self.graph[node2]: # so we don't add a duplicate
                self.graph[node2][reverse_relationship] = set()
            self.graph[node2][reverse_relationship].add(node1)

            if is_new:
                self.tag_usage[node2] += 1

        elif relationship == "is_tag_of":
            reverse_relationship = "has_tag"
            if reverse_relationship not in self.graph[node2]: # so we don't add a duplicate
                self.graph[node2][reverse_relationship] = set()
            self.graph[node2][reverse_relationship].add(node1)

        elif relationship == "is_by_artist":
            reverse_relationship = "has_track"
            if reverse_relationship not in self.graph[node2]: # so we don't add a duplicate
                self.graph[node2][reverse_relationship] = set()
            self.graph[node2][reverse_relationship].add(node1)

        elif relationship == "has_track":
            reverse_relationship = "is_by_artist"
            if reverse_relationship not in self.graph[node2]: # so we don't add a duplicate
                self.graph[node2][reverse_relationship] = set()
            self.graph[node2][reverse_relationship].add(node1)


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
            return None
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

    '''
    Returns List of Top Tags, Amount in Graph
    Input: (optional) Top Amount to Return
    Returns: Returns list of top tags in form [Tag, Amount Used]
    '''
    def get_top_tags(self, top=10):

        print(self.tag_usage.items())
        sorted_tags = sorted(self.tag_usage.items(), key=lambda x: x[1], reverse=True)
        return sorted_tags[:top]
