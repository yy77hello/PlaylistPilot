from TrackGraph import TrackGraph  # Import TrackGraph class

def build_song_tag_graph(playlist):
    """
    Build a graph for the relationships between songs and their tags
    based on the songs in the playlist we provide

    Returns:
        TrackGraph: A TrackGraph object representing the song to tag relationships.
    """
    track_graph = TrackGraph()  # Create an instance of TrackGraph

    for song in playlist.get_songs():  # Iterate through the songs in the playlist
        song_title = song['track_name']  # Get the song title (or a unique identifier)
        track_graph.add_node(song_title)  # Add the song as a node to the graph

        tags = song.get('lastfm_tags', [])  # Get the list of tags for the song
        for tag in tags:
            track_graph.add_edge(song_title, tag, "has_tag")  # Add an edge from the song to each tag

    return track_graph


