from dotenv import load_dotenv
import os
import pylast

load_dotenv()  # loads from .env into this dotenv

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_SECRET = os.getenv("LASTFM_API_SECRET")
# SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
# SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

print(LASTFM_API_KEY)
print(LASTFM_API_SECRET)

# Creating a variable that stores our connection to last.f,
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

print(get_track_tags(get_lastfm_track("Brian Eno", "Emerald and Stone")))