from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env into this dotenv

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_API_SECRET = os.getenv("LASTFM_API_SECRET")
# SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
# SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

print(LASTFM_API_KEY)
print(LASTFM_API_SECRET)