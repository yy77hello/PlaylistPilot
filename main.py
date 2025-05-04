from Playlist import Playlist
from api_access import *
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

# Create Playlist Datatype
my_playlist = Playlist("My Playlist")

# Takes a link to a Spotify Playlist and converts to a playlist graph type
def spotify_playlist_to_playlist(playlist_link):
    # Retrieve playlist spotipy object 
    playlist_id = get_playlist_id_from_link(playlist_link)
    found_playlist = sp.playlist_tracks(playlist_id)
    
    # Get all tracks from playlist
    tracks = found_playlist['items']
    while found_playlist['next']:
        found_playlist = sp.next(found_playlist)
        tracks.extend(found_playlist['items'])
        
    # Loop through found tracks and add them to the playlist graph
    for track in tracks:
        track_title = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        track_info = get_full_song_data(track_title,track_artist)
        my_playlist.add_song(track_info)


# Gets top track for each of the top 10 tracks
def get_recommendations(top_tags):
    recommendations = []
    # Iterate through tags to find the top track for that tag
    for tag_name in top_tags:
        # Get top 25 tracks for tag
        tag = network.get_tag(tag_name[0])
        top_track = get_tag_top_tracks(tag, 25)
        # Loop through tag's top tracks incase there are duplicates
        for track in top_track:
            track_name = track.item.title
            track_artist = track.item.artist.name
            track_input = [track_artist, track_name]
            # Check if track is already in recommendations
            if track_input not in recommendations:
                # Add track to recommendation list
                recommendations.append(track_input)
                break
    # Iterate through recommendations to add tag related tag
    # This is done separately to prevent the same song appearing for different tags
    for i in range(0,len(recommendations)):
        recommendations[i].append(top_tags[i][0])
    # Outputs Array of Top Songs: [Artist, Track Name, Related Tag]
    return recommendations

'''
song1_info = get_full_song_data("Clarity", "Zedd")
my_playlist.add_song(song1_info)

song2_info = get_full_song_data("Pay No Mind", "Madeon")# Misspelled on purpose to see that it recognized it to "Julianna Barwick"
my_playlist.add_song(song2_info)

# Lets try adding the same song again to test the duplicate check
my_playlist.add_song(song1_info) # "Emerald and Stone", "Brian Eno"

# Lets try adding a song that might not be found (should return None)
song3_info = get_full_song_data("Nonexistent Song", "Unknown Artist")
my_playlist.add_song(song3_info)
'''



'''
# Example usage: Get tags for a song
song_to_query = "Clarity"  # Or any song from your playlist
tags_for_song = song_tag_graph.get_connected_nodes(song_to_query, "has_tag")
print(f"\nTags for '{song_to_query}': {tags_for_song}")

# Example usage: Get songs for a tag
tag_to_query = "dance"
songs_with_tag = song_tag_graph.get_connected_nodes(tag_to_query, "is_tag_of")  # This will only work if you add the reverse relationship.
print(f"\nSongs with tag '{tag_to_query}': {songs_with_tag}")
'''

# Main Method
if __name__ == "__main__":
    while True:
        my_playlist = Playlist("My Playlist")
        input_playlist_link = input("Enter playlist link: ")
        spotify_playlist_to_playlist(input_playlist_link)

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

        # Print all tracks that have the dance tag in playlist graph
        print("Dance Tag:", song_tag_graph.get_all_relationships("dance"))

        # Print Top 10 Tags in the playlist Graph
        print("Top 10 Tags:", song_tag_graph.get_top_tags(10))

        # Test to print out the top 10 recommended songs based on each of the top tags
        index = 0
        for recommended_track in get_recommendations(song_tag_graph.get_top_tags()):
            index += 1
            print(str(index) + ": " + recommended_track[0],"-",recommended_track[1],"- Tags:",recommended_track[2].capitalize())
