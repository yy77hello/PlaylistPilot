class Playlist:
    def __init__(self, name):
        # Create a new playlist with a name (ex 'Liked Songs', 'Recommendations')
        self.name = name
        self.songs = []  # List to store song dictionaries

    def add_song(self, song_data):
        # Add a song (represented as a dictionary) to the playlist only if the song_data is valid song and also not already in the playlist
        if song_data is not None and song_data not in self.songs:
            self.songs.append(song_data)
            print(f"Added to playlist: {song_data.get('track_name', 'Unknown Song')}") # Added a print here for convenience

        elif song_data in self.songs:
            print(f"{song_data.get('track_name', 'Unknown Song')} is already in the playlist.")

    def remove_song(self, song_data):
        # Remove a song (represented as a dictionary) from the playlist, if it exists
        if song_data in self.songs:
            self.songs.remove(song_data)
            print(f"Removed from playlist: {song_data.get('track_name', 'Unknown Song')}") #

        else:
            print(f"{song_data.get('track_name', 'Unknown Song')} not found in playlist.")


    def get_songs(self):
        # Return the list of songs in the playlist
        return self.songs
