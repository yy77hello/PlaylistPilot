class Playlist:
    def __init__(self, name):
        # Create a new playlist with a name (ex 'Liked Songs', 'Recommendations')
        self.name = name
        self.songs = []  # List to store song titles

    def add_song(self, song):
        # Add a song to the playlist if its not already in there
        if song not in self.songs:
            self.songs.append(song)

    def remove_song(self, song):
        # Remove a song from the playlist, if it exists
        if song in self.songs:
            self.songs.remove(song)

    def get_songs(self):
        # Return the list of songs in the playlist
        return self.songs
