class Playlist:
    def __init__(self, name):
        # Create a new playlist with a name (ex 'Liked Songs', 'Recommendations')
        self.name = name
        self.songs = []  # List to store song dictionaries

    def add_song(self, song_data):
        # Add a song (represented as a dictionary) to the playlist if it's not already in there
        if song_data not in self.songs:
            self.songs.append(song_data)

    def remove_song(self, song_data):
        # Remove a song (represented as a dictionary) from the playlist, if it exists
        if song_data in self.songs:
            self.songs.remove(song_data)

    def get_songs(self):
        # Return the list of songs in the playlist
        return self.songs
