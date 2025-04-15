from dotenv import load_dotenv
import os
import pylast
import spotipy
# from spotipy.oauth2 import SpotifyOAuth # If using user authentication (for working with user data from spotify)

# loads from .env into this dotenv
if not load_dotenv():
    print("Cant find the env file")

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_SECRET = os.getenv("LASTFM_API_SECRET")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://localhost:8080" # Can also use 127.0.0.1

# Sp is an object holding spotify client locally
sp = spotipy.Spotify() # No authentication client, still should be good for searching functionality that we need

# We can use this if we want to use an authenticated spotify client, useful if we want to work with users data
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
#                                                client_secret=SPOTIFY_CLIENT_SECRET,
#                                                redirect_uri=SPOTIFY_REDIRECT_URI,
#                                                scope="user-library-read"))

def search_spotify_track(track_name, artist_name):
    # limit = 1 argument means that this will only return one song. Consider playing around with this value if we want to implement user choice between search options
    results = sp.search(q=f"track:{track_name} artist:{artist_name}", type="track", limit=1)
    if results and results['tracks']['items']: # Wouldn't pass if we got an error in searching or nothing came up
        return results['tracks']['items'][0]
    return None

def get_full_song_data(track_name, artist_name):

    track = search_spotify_track(track_name, artist_name)
    spotify_data = {}
    if track:
        spotify_data = {
            "track_name": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            # You can also get other data from the song
        }

    if spotify_data:
        lastfm_track = get_lastfm_track(spotify_data['artist'], spotify_data['track_name'])
        if lastfm_track:
            tags = get_track_tags(lastfm_track)
            tag_names = [tag.item.get_name() for tag in tags] # List comprehension
            full_data = {
                **spotify_data,  # Include Spotify data. This will do dictionary unpacking to store key-value pairs that we had in our earlier spotify data dict
                "lastfm_tags": tag_names,  # Add Last.fm tags
            }
            return full_data
        else:
            return spotify_data  # Return Spotify data even if Last.fm doesn't have it
    return None

# For testing
# print("LastFM API information loaded from env")
# print(LASTFM_API_KEY)
# print(LASTFM_API_SECRET)
# print("Spotify API information loaded from env")
# print(SPOTIFY_CLIENT_ID)
# print(SPOTIFY_CLIENT_SECRET)
print("Redirect URL: ", SPOTIFY_REDIRECT_URI)

# Creating a variable that stores our connection to last.fm
network = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET)

"""
Searches for a track on Last.fm.
Inputs: Artist and track name
Returns: A pylast.Track object if found, none otherwise.
"""
def get_lastfm_track(artist, track_name):
    track = network.get_track(artist, track_name)
    return track

"""
Gets tags for a track on Last.fm.
Inputs: Track object 
Returns: A list of Tag objects
"""
def get_track_tags(track):
    if track:
        tags = track.get_top_tags()
        return tags
    return [] # Only goes here if no valid track

def get_tag_tracks(tag):
    if tag:
        tracks = tag.get_top_tracks()
        return tracks
    return [] # Only goes here if no valid track

print("Testing getting lastfm song data:", get_lastfm_track("Brian Eno", "Emerald and Stone"))
print("Testing getting lastfm tag data:", get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone")))
# print("Testing getting lastfm tracks per tag data:", get_tag_tracks(get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone"))))
print("First tag:", get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone"))[0].item)
for i in range(6):
    print("Tag", i, ":", get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone"))[i].item)
# help(pylast.TopItem)