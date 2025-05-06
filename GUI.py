import tkinter as tk
from tkinter import *
from main import get_recommendations, spotify_playlist_to_playlist
from tkinter import PhotoImage, font

# Create the main window
window = tk.Tk()
window.title("PlaylistPilot")
window.geometry("900x600")
logo = PhotoImage(file="logo.PNG")
resized_logo_subsample = logo.subsample(8, 8)


def main_screen():
    clear_screen()
    logo_label = tk.Label(window, image=resized_logo_subsample)
    logo_label.pack(side=TOP)

    # Add a label widget
    label = tk.Label(window, text="Playlist Pilot", font=font.Font(size=22))
    label.pack()

    selected_option = tk.StringVar()
    options = ["Choose Option", "Input Song", "Input Playlist"]
    selected_option.set(options[0])

    def update_screen():
        if selected_option.get() == "Input Song":
            show_screen1()
        elif selected_option.get() == "Input Playlist":
            show_screen2()

    option_menu = tk.OptionMenu(window, selected_option, *options, command=lambda _: update_screen())
    option_menu.config(width=10)
    option_menu.pack()
    update_screen()

# Choice Options
def show_screen1():
    clear_screen()
    button = tk.Button(window, text="Back", command=lambda: main_screen())
    button.pack(side=LEFT)
    button = tk.Button(window, text="Done", command=window.destroy)
    button.pack(side=RIGHT)

    logo_label = tk.Label(window, image=resized_logo_subsample)
    logo_label.pack(side=TOP)
    label = tk.Label(window, text="Playlist Pilot", font=font.Font(size=22))
    label.pack(side=TOP)
    label = tk.Label(window, text="Enter Song:")
    label.pack()

    song_name = tk.Entry(window, bg="#676767")
    song_name.pack()

    label = tk.Label(window, text="Enter Artist:")
    label.pack()

    artist_name = tk.Entry(window, bg="#676767")
    artist_name.pack()

    button = tk.Button(window, text="Submit")
    button.pack()


def show_screen2():
    clear_screen()
    button = tk.Button(window, text="Back", command=lambda: main_screen())
    button.pack(side=LEFT)
    button = tk.Button(window, text="Done", command=window.destroy)
    button.pack(side=RIGHT)
    logo_label = tk.Label(window, image=resized_logo_subsample)
    logo_label.pack()

    label = tk.Label(window, text="Playlist Pilot", font=font.Font(size=22))
    label.pack()

    label = tk.Label(window, text="Enter Playlist Link:")
    label.pack()

    playlist = tk.Entry(window, bg="#676767")
    playlist.pack()

    button = tk.Button(window, text="Submit")
    button.pack()


def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()

logo_label = tk.Label(window, image=resized_logo_subsample)
logo_label.pack(side=TOP)

# Add a label widget
label = tk.Label(window, text="Playlist Pilot", font=font.Font(size=22))
label.pack()

button = tk.Button(window, text="Start", command=lambda: main_screen(), height=3, width=10)
button.pack()

# Start the main event loop
window.mainloop()
