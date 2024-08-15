# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 14:32:09 2024

@author: ahigh
"""

# Import modules
from hidden import CLIENT_ID, CLIENT_SECRET, SPOTIPY_REDIRECT
import pandas as pd
import time
from itertools import cycle
import tkinter as tk 
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font
import customtkinter 
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Read in vibes playlist
df = pd.read_csv("https://raw.githubusercontent.com/highad93/track_artists/main/song_vibes.csv").drop(['Unnamed: 0'], axis=1)

# Sortvalues by selected vibe variable
df = df.sort_values(by='vibe2') # To create list in alphabetic order

# Check counts of song per vibe
vibe_counts = df['vibe2'].value_counts(dropna=False)


# Now we build the GUI to make song selection
# Create root/window
root = tk.Tk()
root.title("Create your playlist here!")
root.geometry("800x1000")


# Add widgets to root

#Add a label with instructions for adding a playlist name
name_label = tk.Label(root, text="Enter name for your new playlist:")
name_label.config(font=['Arial', 16])
name_label.pack(pady=5)


# Create field for user entry
entry = Entry()
entry.config(font=['Ink Free', 16])
entry.pack()

# Add a label with instructions for selcting vibe
vibe_label = tk.Label(root, text="Select a vibe from the menu:")
vibe_label.config(font=['Arial', 16]) # Adjust font and size of label
vibe_label.pack(pady=5) # Pack label onto root

# Create selection vars
vibe_selection = tk.StringVar(root)
duration_selection = tk.StringVar()
spotify_add_selection = tk.StringVar()

# Create a dropdown menu with options for vibe
vibe_options = list(df['vibe2'].unique())
vibe_dropdown = tk.OptionMenu(root, vibe_selection, *vibe_options)
vibe_dropdown.config(font=['Arial',16])
vibe_dropdown.pack()

# Add a label with instruction for slecting playlist duration
duration_label = tk.Label(root, text="How long of a playlist do you want?")
duration_label.config(font=['Arial', 16]) # Adjust font and size of label
duration_label.pack(pady=5) # Pack label onto root

# Create a dropdown menu with options for duration
duration_options = ["30 minutes", "60 minutes", "90 minutes", "120 minutes", "150 minutes", "180 minutes"]
duration_dropdown = tk.OptionMenu(root, duration_selection, *duration_options)
duration_dropdown.config(font=['Arial',16])
duration_dropdown.pack()




duration_dict = {"30 minutes": 35, 
                    "60 minutes" : 65,
                    "90 minutes" : 95,
                    "120 minutes" :125,
                    "150 minutes" :155,
                    "180 minutes" :185}

# This is the generate playlist button
def click_button():
    
    playlist_name = entry.get() #Get playlist name from user entry
    my_label.config(text='generating ' + entry.get() + ' playlist......', font=['Arial',11])
    your_playlist.config(text= entry.get() , font=['Arial',16])
    print(playlist_name)
    
    # Filter by vibe selection
    selected_vibe_df = df[df['vibe1']==vibe_selection.get()]
    
    # Get the duration of all songs with that vibe in minutes (duration is in millisecond)
    total_duration = (selected_vibe_df['duration'].sum() / 60000)
    print( selected_vibe_df)
    print(total_duration)
    
    
    
    # If the total duration of a selected vibe is less than the selected duration, alert user
    if total_duration < duration_dict[duration_selection.get()]:
        sorry.config(text = 'sorry there are not enough songs to fulfill request, select a shorter duration')
        print ('sorry there are not enough songs to fulfill request, select a shorter duration')
    
    else:
        sorry.config(text="")
        # Remove songs until duration is less than or equal to selected suration
        while total_duration >= duration_dict[duration_selection.get()]:
            remove =  selected_vibe_df.sample(n=1) # Randomly select 1 song
            selected_vibe_df = selected_vibe_df.drop(remove.index)
            total_duration = (selected_vibe_df['duration'].sum() / 60000) #Recalculate total duration
        #print(selected_vibe_df, total_duration)
        selected_songs = list(zip(selected_vibe_df['track_name'], selected_vibe_df['artist_name']))
        selected_song_ids = list((selected_vibe_df['song_id']))
        print(selected_song_ids)
        
        # Clear items if button is clicked more than once
        for item in your_songs.get_children():
            your_songs.delete(item)
        
        print(selected_songs)
        iid = 0
        iid1 = 0
        for song in selected_songs:
            #print(song)
            # Insert songs into treeview for display
            your_songs.insert(parent='', index='end', iid = iid , values = song)
            iid +=1
        for song_id in selected_song_ids:
            # Insert songs into secondary treeview for Spotify connection
            song_ids.insert(parent='', index='end', iid = iid1 , values = song_id)
            iid1 +=1
        your_songs.pack() 
        spotify_add_label.pack(pady=5)
        spotify_add_dropdown.pack()
        spotify_button.pack()

        
        
    
 
# Create generate playlist button - upon click "click_button" function will run
button = tk.Button(root, text="Generate Playlist!", command=click_button)
button.config(font = ['Arial',16])
button.pack(pady=5)


# Creating a label to show it's working
my_label = Label(root, text='')
my_label.pack()

# Title for playlist
your_playlist = Label(root, text= '', font = font.Font(family="Helvetica", size=16, weight="bold"), fg="blue")
your_playlist.pack()

# Error message, adjust selections
sorry = Label(root, text="")
sorry.pack()



# Treeview to display select songs
your_songs = ttk.Treeview(root)


# Define columns of tree
your_songs['columns'] = ('TRACK NAME', 'ARTIST')

# Format treeview
your_songs.column("#0", width=0, stretch=NO )
your_songs.column("TRACK NAME", width=150, anchor =W)
your_songs.column("ARTIST", width=150, anchor=CENTER)

your_songs.heading("TRACK NAME", text='Track Name', anchor = W)
your_songs.heading("ARTIST", text= 'Artist Name', anchor=W)


# Treeview for song ids - this won't actually be displayed
song_ids = ttk.Treeview(root)
song_ids['columns'] = ("SONG_ID")
song_ids.column("#0", width = 0, stretch=NO)
song_ids.column("SONG_ID", width =150, anchor  = W)
song_ids.heading("SONG_ID", text = 'Song Id', anchor = W)


#Style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=(None, 12))
style.configure("Treeview.Heading", font=(None, 16))

# Add a label with instruction for adding playlist to spotify
spotify_add_label = tk.Label(root, text="Do you want to add playlist to your spotify library?")
spotify_add_label.config(font=['Arial', 16]) # Adjust font and size of label

# Create dropdown for adding songs to spotify
spotify_add_options = ["Yes, this is lit!", "No, this is trash!"]
spotify_add_dropdown = tk.OptionMenu(root, spotify_add_selection, *spotify_add_options)
spotify_add_dropdown.config(font=['Arial',16])


# Add a label with instruction for adding playlist to spotify
spotify_user_label = tk.Label(root, text="Enter your spotify user id:")
spotify_user_label.config(font=['Arial', 16]) # Adjust font and size of label


# Create field for user entry for Spotify id
entry1 = Entry()
entry1.config(font=['Ink Free', 16])


# User satisfaction button - if user likes playlist prompt for user id, if not clear the playlist 
def new_window():
    if spotify_add_selection.get() == 'Yes, this is lit!':
        spotify_user_label.pack()
        entry1.pack()
        spotify_button1.pack()
    else:
        
        for item in your_songs.get_children():
            your_songs.delete(item)
        
        
        #win.mainloop()
        print('yup!')

# Create go button
spotify_button = tk.Button(root, text="Gooo!", command=new_window)
spotify_button.config(font = ['Arial',16] )

# This function collects the users Spotify ID, create their new playlist and add tracks to the playlist
def add_to_spotify():
    scope = "playlist-modify-public"
    username = entry1.get()
    print (username)
    try:
        sorry1.config(text="redirecting  to your spotify playlist")
        sorry1.pack()
        # Generate access token
        token = SpotifyOAuth(client_id = CLIENT_ID, client_secret= CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT, 
                             scope=scope, username=username)
        # Define Spotify Object
        spotifyObject = spotipy.Spotify(auth_manager= token)
        # Create playlist
        spotifyObject.user_playlist_create(user=username, name= entry.get(), public = True, description = "")
        preplaylist = spotifyObject.user_playlists(user=username)
        playlist = preplaylist['items'][0]['id']
        list_of_song_ids = []
        for line in song_ids.get_children():
            print (line)
            for value in song_ids.item(line)['values']:
                print(value) 
                list_of_song_ids.append(value)
        # Add tracks to playlist    
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id = playlist, tracks = list_of_song_ids)
        # Open playlist in browser
        webbrowser.open( 'https://open.spotify.com/playlist/{}'.format(playlist))
    except:
        # If invalid user id is entered
        sorry1.config(text='is that really your username? try again')
        sorry1.pack() 
    return None

# Create final add to spotify button
spotify_button1 = tk.Button(root, text="ADD TO MY SPOTIFY ACCOUNT", command=add_to_spotify)
spotify_button1.config(font = ['Arial',16] )

# Error message, adjust selections
sorry1 = Label(root, text="")


# Run/open Gui 
root.mainloop()



