# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:38:25 2024

@author: ahigh
"""

from hidden import CLIENT_ID, CLIENT_SECRET
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from get_spotify_creds import get_spotify_creds
import json
import pandas as pd
import time

# Read in complete dataset

df = pd.read_csv("https://raw.githubusercontent.com/highad93/track_artists/main/datawithgenres.csv").drop(['Unnamed: 0'], axis=1)

# Create list of unique playlist ids
playlist_lst = list(df['playlist_id'].unique())


        
        
# CONNECT TO SPOTPY API 
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

    
# Define function to get playlist description and image
def get_playlist_info(playlist_id: str, limit: int = 10, access_token:str = None) -> list:
    """
    Returns a list of [playlist_id, description, image]
    :param playlist_id (str): The playlist ID to query.
    """

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    if access_token == None:
        access_token = get_spotify_creds()

    headers = {"Authorization": "Bearer " + access_token}

    params = {"limit": limit}
    response = requests.get(url, headers=headers, params=params)


    print(response.status_code)

    if response.status_code == 200:
      data = response.json()
      description = data['description']
      image = data['images'][0]['url']
      name =  data['name']

      return [playlist_id, description, image, name]
      #return data
      
    else:
      return response.text

#Retain playlist info in separate list

playlist_info = []
for playlist_id in playlist_lst:
    print(playlist_id)
    p_info = get_playlist_info(playlist_id)
    playlist_info.append(p_info)
    time.sleep(20)
# Create df from  list

playlist_info_df = pd.DataFrame(playlist_info, columns =['playlist_id','description','image','name'])

# Merge with songs

playlist_info_df.to_csv('playlist_info1.csv')

