# PlaylistPilot

<img src="./logo.jpg" alt="Playlist Pilot logo" width="80%">


## Abstract
This project aims to develop a music recommendation system that allows users to create personalized playlists based on their song selections and the relationships between song tags. The system will utilize the Spotify and Last.fm APIs to retrieve music data and user input, organizing this information using tree and graph data structures. A recommendation algorithm will analyze tag relationships to suggest relevant tracks, offering users a dynamic and intuitive way to discover new music based on their existing preferences.

## Project Goals
- Enable users to search for and select songs from the Spotify library.
- Match selected songs to their entries in Last.fm for use with Last.fm API methods.
- Organize song data into a hierarchical tree structure.
- Represent tag relationships using a graph data structure.
- Generate personalized playlists based on user input and tag analysis.
- Provide a user-friendly interface for playlist interaction.

## Objectives
- Design and implement API integrations for Spotify and Last.fm.
- Develop data retrieval and structuring mechanisms for song data.
- Implement tree and graph data structures for organizing song data and tag relationships.
- Design and implement a recommendation algorithm for playlist generation.
- Develop a user interface for playlist creation, interaction, and data visualization.

## Data Structures
- **Playlist:** List to store user-selected songs.
- **Tree:** Hierarchical structure for song organization (artist, album, track).
- **Graph:** Network representing relationships between song tags.

## APIs
- **Spotify API via Spotipy:** Song search, metadata retrieval.
- **Last.fm API via Pylast:** Song tag retrieval, track recommendations based on tags.

## Dependencies
- **pylast:** For interacting with the Last.fm API. Install with:  

     pip3 install pylast

  
- **python-dotenv:** For loading environment variables from a .env file. Install with: 

    pip3 install python-dotenv


