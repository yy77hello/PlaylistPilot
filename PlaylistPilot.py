from Playlist import Playlist
from api_access import *
from graph_builder import build_song_tag_graph
import tkinter as tk
from tkinter import *
from tkinter import PhotoImage, font

# Create Playlist Datatype
my_playlist = Playlist('My Playlist')

# Create Main Window
window = tk.Tk()
window.title('PlaylistPilot')
window.geometry('1000x600')
logo = PhotoImage(file='logo.PNG')
resized_logo_subsample = logo.subsample(8, 8)

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

def main_screen():
    clear_screen()

    # Bottom frame for navigation buttons
    nav_frame = tk.Frame(window)
    nav_frame.pack(side='bottom', fill='x', pady=10)

    # Button to close program
    button_done = tk.Button(nav_frame, text='Done', command=window.destroy)
    button_done.pack(side='right', padx=20)

    # Logo
    label_logo = tk.Label(window, image=resized_logo_subsample)
    label_logo.pack(side='top')

    # Title
    label_title = tk.Label(window, text='Playlist Pilot', font=font.Font(size=22))
    label_title.pack()

    # Option Selector
    selected_option = tk.StringVar()
    options = ['Input Song', 'Input Playlist','Recommendations']
    selected_option.set("Choose Option")
    def update_screen():
        if selected_option.get() == 'Input Song':
            show_screen_song()
        elif selected_option.get() == 'Input Playlist':
            show_screen_playlist()
        elif selected_option.get() == 'Recommendations':
            show_screen_recommended()
    option_menu = tk.OptionMenu(window, selected_option, *options, command=lambda _: update_screen())
    option_menu.config(width=15)
    option_menu.pack(pady=10)
    update_screen()

    # Playlist output
    listbox_playlist = tk.Listbox(window)
    clear_button = tk.Button(window, text='Clear Playlist', command=lambda: clear_playlist(listbox_playlist))
    clear_button.pack(pady=(0, 20))

    # Frame
    frame_playlist = tk.Frame(window, bg='white')
    frame_playlist.pack(fill='both', expand=True, pady=10, padx=25)

    # Scrollbar
    scrollbar_playlist = tk.Scrollbar(frame_playlist, orient='vertical')
    scrollbar_playlist.pack(side='right', fill='y')

    # Listbox
    listbox_playlist = tk.Listbox(frame_playlist, bg='white', fg='black', yscrollcommand=scrollbar_playlist.set, font=("Courier", 16))
    listbox_playlist.pack(side='left', fill='both', expand=True)
    scrollbar_playlist.config(command=listbox_playlist.yview)

    # Clear Listbox
    listbox_playlist.delete(0, tk.END)

    # Listbox Header
    header = f"{'Index':<6} {'Artist':<25} {'Track':<35}"
    listbox_playlist.insert(tk.END, header)
    listbox_playlist.insert(tk.END, "-" * len(header))

    # Display songs from playlist
    for index, song in enumerate(my_playlist.get_songs(), start=1):
        artist = song.get('artist', 'Unknown Artist')
        track = song.get('track_name', 'Unknown Track')
        formatted = f"{index:<6} {artist:<25} {track:<35}"
        listbox_playlist.insert(tk.END, formatted)

    listbox_playlist.focus_force()

# Choice Options
def show_screen_recommended():
    clear_screen()

    # Bottom frame for navigation buttons
    nav_frame = tk.Frame(window)
    nav_frame.pack(side='bottom', fill='x', pady=10)

    # Button to return to main screen
    button_back = tk.Button(nav_frame, text='Back', command=main_screen)
    button_back.pack(side='left', padx=20)

    # Button to close program
    button_done = tk.Button(nav_frame, text='Done', command=window.destroy)
    button_done.pack(side='right', padx=20)

    # Logo
    label_logo = tk.Label(window, image=resized_logo_subsample)
    label_logo.pack(side='top')

    # Title
    label_title = tk.Label(window, text='Playlist Pilot', font=font.Font(size=22))
    label_title.pack(side='top')

    # Frame
    frame_recommended = tk.Frame(window, bg='white')
    frame_recommended.pack(fill='both', expand=True, pady=10, padx=25)

    # Scrollbar
    scrollbar_recommended = tk.Scrollbar(frame_recommended, orient='vertical')
    scrollbar_recommended.pack(side='right', fill='y')

    # Listbox
    listbox_recommended = tk.Listbox(frame_recommended, bg='white', fg='black',
                                     yscrollcommand=scrollbar_recommended.set, font=("Courier", 16))
    listbox_recommended.pack(side='left', fill='both', expand=True)
    scrollbar_recommended.config(command=listbox_recommended.yview)

    # Get top recommendations
    song_tag_graph = build_song_tag_graph(my_playlist)
    recommendations = get_recommendations(song_tag_graph.get_top_tags())

    # Clear listbox before inserting new items
    listbox_recommended.delete(0, tk.END)

    # Listbox Header
    header = f"{'Index':<6} {'Artist':<25} {'Track':<35} {'Tag':<15}"
    listbox_recommended.insert(tk.END, header)
    listbox_recommended.insert(tk.END, "-" * len(header))

    # Insert each formatted recommendation
    for index, track in enumerate(recommendations, start=1):
        artist = track[0]
        title = track[1]
        tag = track[2].capitalize()

        formatted = f"{index:<6} {artist:<25} {title:<35} {tag:<15}"
        listbox_recommended.insert(tk.END, formatted)

    # Forces window to load properly, as it appears like its invisible initially
    listbox_recommended.focus_force()

def show_screen_song():
    clear_screen()

    # Bottom frame for navigation buttons
    nav_frame = tk.Frame(window)
    nav_frame.pack(side='bottom', fill='x', pady=10)

    # Button to return to main screen
    button_back = tk.Button(nav_frame, text='Back', command=main_screen)
    button_back.pack(side='left', padx=20)

    # Button to close program
    button_done = tk.Button(nav_frame, text='Done', command=window.destroy)
    button_done.pack(side='right', padx=20)

    # Logo
    label_logo = tk.Label(window, image=resized_logo_subsample)
    label_logo.pack(side='top')

    # Title
    label_title = tk.Label(window, text='Playlist Pilot', font=font.Font(size=22))
    label_title.pack(side='top')

    # Song title prompt
    label_song_prompt = tk.Label(window, text='Enter Song:')
    label_song_prompt.pack()

    # Song title user input
    entry_song_title = tk.Entry(window,
                                bg='white',
                                fg='black',
                                font=("Arial", 16),
                                width=30,
                                justify='center',
                                highlightthickness=1,
                                highlightbackground='gray',
                                highlightcolor='blue',
                                insertbackground='black')
    entry_song_title.pack(padx=10, ipady=2)

    # Song artist prompt
    label_artist_prompt = tk.Label(window, text='Enter Artist:')
    label_artist_prompt.pack()

    # Song artist user input
    entry_artist = tk.Entry(window,
                            bg='white',
                            fg='black',
                            font=("Arial", 16),
                            width=30,
                            justify='center',
                            highlightthickness=1,
                            highlightbackground='gray',
                            highlightcolor='blue',
                            insertbackground='black')
    entry_artist.pack(padx=10, ipady=2)

    # Submit Button
    listbox_playlist = tk.Listbox(window)
    button_submit = tk.Button(window, text='Submit', command=lambda: submit_song(entry_artist, entry_song_title, listbox_playlist))
    button_submit.pack()

    # Frame
    frame_playlist = tk.Frame(window, bg='white')
    frame_playlist.pack(fill='both', expand=True, pady=10, padx=25)

    # Scrollbar
    scrollbar_playlist = tk.Scrollbar(frame_playlist, orient='vertical')
    scrollbar_playlist .pack(side='right', fill='y')

    # Listbox
    listbox_playlist = tk.Listbox(frame_playlist, bg='white', fg='black', yscrollcommand=scrollbar_playlist.set, font=("Courier", 16))
    listbox_playlist.pack(side='left', fill='both', expand=True)
    scrollbar_playlist.config(command=listbox_playlist.yview)

    # Clear Listbox
    listbox_playlist.delete(0, tk.END)

    # Listbox Header
    header = f"{'Index':<6} {'Artist':<25} {'Track':<35}"
    listbox_playlist.insert(tk.END, header)
    listbox_playlist.insert(tk.END, "-" * len(header))

    # Display songs from playlist
    for index, song in enumerate(my_playlist.get_songs(), start=1):
        artist = song.get('artist', 'Unknown Artist')
        track = song.get('track_name', 'Unknown Track')
        formatted = f"{index:<6} {artist:<25} {track:<35}"
        listbox_playlist.insert(tk.END, formatted)

    # Forces window to load properly, as it appears like its invisible initially
    entry_song_title.focus_force()

# Show Playlist Adding Screen
def show_screen_playlist():
    # Reset window
    clear_screen()

    # Bottom frame for navigation buttons
    nav_frame = tk.Frame(window)
    nav_frame.pack(side='bottom', fill='x', pady=10)

    # Button to return to main screen
    button_back = tk.Button(nav_frame, text='Back', command=main_screen)
    button_back.pack(side='left', padx=20)

    # Button to close program
    button_done = tk.Button(nav_frame, text='Done', command=window.destroy)
    button_done.pack(side='right', padx=20)

    # Logo
    label_logo = tk.Label(window, image=resized_logo_subsample)
    label_logo.pack()

    # Title
    label_title = tk.Label(window, text='Playlist Pilot', font=font.Font(size=22))
    label_title.pack()

    # Playlist Prompt
    label_playlist_prompt = tk.Label(window, text='Enter Spotify Playlist Link:')
    label_playlist_prompt.pack()

    # Playlist Link User Input
    entry_playlist = tk.Entry(window,
                              bg='white',
                              fg='black',
                              font=("Arial", 14),
                              width=60,
                              highlightthickness=1,
                              highlightbackground='gray',
                              highlightcolor='blue',
                              insertbackground='black')
    entry_playlist.pack(padx=10, ipady=6)

    # Submit Button
    listbox_playlist = tk.Listbox(window)
    button_playlist = tk.Button(window, text='Submit', command=lambda: submit_link(entry_playlist, listbox_playlist))
    button_playlist.pack(pady=5)

    # Frame
    frame_playlist = tk.Frame(window, bg='white')
    frame_playlist.pack(fill='both', expand=True, pady=10, padx=25)

    # Scrollbar
    scrollbar_playlist = tk.Scrollbar(frame_playlist, orient='vertical')
    scrollbar_playlist.pack(side='right', fill='y')

    # Playlist Output Listbox
    listbox_playlist = tk.Listbox(frame_playlist, bg='white', fg='black', yscrollcommand=scrollbar_playlist.set, font=("Courier", 16))
    listbox_playlist.pack(side='left', fill='both', expand=True)
    scrollbar_playlist.config(command=listbox_playlist.yview)

    # Clear Listbox
    listbox_playlist.delete(0, tk.END)

    # Listbox Header
    header = f"{'Index':<6} {'Artist':<25} {'Track':<35}"
    listbox_playlist.insert(tk.END, header)
    listbox_playlist.insert(tk.END, "-" * len(header))

    # Display songs from playlist
    for index, song in enumerate(my_playlist.get_songs(), start=1):
        artist = song.get('artist', 'Unknown Artist')
        track = song.get('track_name', 'Unknown Track')
        formatted = f"{index:<6} {artist:<25} {track:<35}"
        listbox_playlist.insert(tk.END, formatted)

    # Forces window to load properly, as it appears like its invisible initially
    entry_playlist.focus_force()

# Removes all objects from screen, in other words resets the window
def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()

'''
Function for when submit is pressed on the playlist screen
Takes user entered list, retrieves it from spotify,
enters the playlist songs into the playlist graph
and prints it to the listbox
'''
def submit_link(entry_playlist, listbox):
    # Get input link
    input_playlist_link = entry_playlist.get()

    # Check if Link Input
    if not input_playlist_link:
        return

    print("Fetching playlist...")

    # Build playlist and graph
    spotify_playlist_to_playlist(input_playlist_link)

    # Clear Listbox
    listbox.delete(0, tk.END)

    # Listbox Header
    header = f"{'Index':<6} {'Artist':<25} {'Track':<35}"
    listbox.insert(tk.END, header)
    listbox.insert(tk.END, "-" * len(header))

    # Display songs from playlist
    for index, song in enumerate(my_playlist.get_songs(), start=1):
        artist = song.get('artist', 'Unknown Artist')
        track = song.get('track_name', 'Unknown Track')
        formatted = f"{index:<6} {artist:<25} {track:<35}"
        listbox.insert(tk.END, formatted)


'''
Function for when submit is pressed on the song screen:
Takes user input song title and artist, retrieves it from spotify,
enters the song into the playlist graph
and prints it to the listbox
'''
def submit_song(entry_artist, entry_song, listbox):
    # Get song info from inputs and insert into the playlist graph
    artist = entry_artist.get()
    song = entry_song.get()
    song_info = get_full_song_data(song, artist)

    # No Song Found
    if not song_info:
        return

    # If found, add song to playlist graph
    my_playlist.add_song(song_info)

    # Clear Listbox
    listbox.delete(0, tk.END)

    # Listbox Header
    header = f"{'Index':<6} {'Artist':<25} {'Track':<35}"
    listbox.insert(tk.END, header)
    listbox.insert(tk.END, "-" * len(header))

    # Display songs from playlist
    for index, song in enumerate(my_playlist.get_songs(), start=1):
        artist = song.get('artist', 'Unknown Artist')
        track = song.get('track_name', 'Unknown Track')
        formatted = f"{index:<6} {artist:<25} {track:<35}"
        listbox.insert(tk.END, formatted)

def clear_playlist(listbox):
    # Overwrite my_playlist with a new Playlist object
    global my_playlist
    my_playlist = Playlist('My Playlist')
    print("Playlist cleared.")

    # Clear Listbox
    listbox.delete(0, tk.END)

    # Listbox Header
    header = f"{'Index':<6} {'Artist':<25} {'Track':<35}"
    listbox.insert(tk.END, header)
    listbox.insert(tk.END, "-" * len(header))

# Main Method
if __name__ == '__main__':
    # Logo
    label_logo = tk.Label(window, image=resized_logo_subsample)
    label_logo.pack(side='top')

    # Title
    label_title = tk.Label(window, text='Playlist Pilot', font=font.Font(size=22))
    label_title.pack()

    # Create start button
    start_button = tk.Button(window, text='Start', command=lambda: main_screen(), height=3, width=10, font=("Arial", 22))
    start_button.pack(pady=10)

    # Start the main event loop and focuses window.
    window.focus_force()
    window.mainloop()
