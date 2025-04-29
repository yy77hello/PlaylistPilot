from Playlist import Playlist
from api_access import get_full_song_data
from graph_builder import build_song_tag_graph

# ----------------------------------------- #

# Testing to see what tag data output looks like
# print("Testing getting lastfm song data:", get_lastfm_track("Brian Eno", "Emerald and Stone"))
# print("Testing getting lastfm tag data:", get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone")))
# # print("Testing getting lastfm tracks per tag data:", get_tag_tracks(get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone"))))
# print("First tag:", get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone"))[0].item)
# for i in range(6):
#    print("Tag", i, ":", get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone"))[i].item)
# help(pylast.TopItem)

# print(get_full_song_data("Emerald and Stone", "Brian Eno"))

# ----------------------------------------- #

# Testing TrackGraph

# # Testing
#
# track_graph = TrackGraph()
#
# # Add nodes (songs, tags, artists)
# track_graph.add_node("Emerald and Stone")
# track_graph.add_node("ambient")
# track_graph.add_node("Brian Eno")
#
# # Add relationships (edges)
# track_graph.add_edge("ambient", "Emerald and Stone", "is a tag of")
# track_graph.add_edge("Emerald and Stone", "Brian Eno", "is by artist")
#
# # Accessing connected nodes:
# # Get all songs tagged with 'ambient'
# connected_songs = track_graph.get_connected_nodes("ambient", "is a tag of")
# print(connected_songs)  # Output: {'song: Emerald and Stone'}
#
# # Get all artists of the song 'Emerald and Stone'
# connected_artists = track_graph.get_connected_nodes("Emerald and Stone", "is by artist")
# print(connected_artists)  # Output: {'Brian Eno'}
#
# # Get all relationships of a song
# relationships = track_graph.get_all_relationships("Emerald and Stone")
# for relationship, nodes in relationships:
#     print(f"Relationship: {relationship}")
#     print(f"Connected Nodes: {nodes}")

# ----------------------------------------- #

# Testing playlist, tags, and graphs
my_playlist = Playlist("My Playlist")

song1_info = get_full_song_data("Emerald and Stone", "Brian Eno")
my_playlist.add_song(song1_info)

song2_info = get_full_song_data("Inspirit", "Julianna Barwick") # Misspelled on purpose to see that it recognized it to "Julianna Barwick"
my_playlist.add_song(song2_info)

# Lets try adding the same song again to test the duplicate check
my_playlist.add_song(song1_info) # "Emerald and Stone", "Brian Eno"

# Lets try adding a song that might not be found (should return None)
song3_info = get_full_song_data("Nonexistent Song", "Unknown Artist")
my_playlist.add_song(song3_info)

print("\nSongs in my playlist:")
for song in my_playlist.get_songs():
    print(song['track_name'], "-", song['artist'])

# Build the graph
song_tag_graph = build_song_tag_graph(my_playlist)

# Print the graph (for testing and verification)
print("\nSong-Tag Graph:")
for node, relationships in song_tag_graph.graph.items():
    print(f"\nNode: {node}")
    for relationship, connected_nodes in relationships.items():
        print(f"  {relationship}: {connected_nodes}")

# Example usage: Get tags for a song
song_to_query = "Emerald and Stone"  # Or any song from your playlist
tags_for_song = song_tag_graph.get_connected_nodes(song_to_query, "has_tag")
print(f"\nTags for '{song_to_query}': {tags_for_song}")

# Example usage: Get songs for a tag
tag_to_query = "ambient"
songs_with_tag = song_tag_graph.get_connected_nodes(tag_to_query, "is_tag_of")  # This will only work if you add the reverse relationship.
print(f"\nSongs with tag '{tag_to_query}': {songs_with_tag}")