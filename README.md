# Spotify Playlist Suggestions 
### Adrianna High, Austin Eck, and Yousra Zouani
# Documentation updated Aug 15, 2024

## About the Project 

The challenge of finding the perfect songs to fit the mood and vibe can be a daunting task. How many of us start a playlist with one or two songs and can’t seem to complete it? Our goal was to do the hard part for Spotify users - building upon previous work in Milestone II, the purpose of this capstone project is to create a music recommendation system that generates music playlists based on user selected “vibe”.  For our purposes, we define the vibe of a song as the desired environment/atmosphere separate and distinct from its musical genre. This process would involve finding songs that fit a particular mood/vibe, building out a graphical user interface (GUI) to allow user selections (their vibe and duration of playlist) and connect that interface directly to Spotify so the playlist can be added to the user’s account automatically. 

The hard part would be mapping vibes onto each song, so we tried a few different approaches to this task. We initially tried to cluster songs based on their various audio features (acousticness,loudness, speechiness, etc). The theory was that songs of a specific vibe would have different characteristics than other vibes - maybe party songs would be higher in tempo, loudness, and danceability but lower in acousticness. An alternate option was to extract topics from the playlist descriptions - the description of the playlist should say something about the type of songs included on the playlist, right? “To linger on your break up, sadness or madness” is pretty telling! Ultimately, the latter option generated vibe labels that made the most sense.

### Getting Started 
1. Clone this repository using:

`git clone https://github.com/highad93/track_artists.git`

2. Install the required libraries: 

`conda install --yes --file requirements.txt`

Or... 

`pip install -r requirements.txt`

3. Rename `hidden_sample.py` as `hidden.py`. 

4. Add your Spotify and Open AI credentials in the appropriate places. 
5. Run the application by running `build_gui_final.py`

`python build_gui.py`

### Data Access Statement 

The data used from this project was collected using the Spotify API. 
In order to collect the data, a Spotify developer account is required. 
Users can sign up for a developer account using their individual Spotify accounts. 
For the purpose of this project, the data collected from the API is available as `datawithgenres.csv`. 

Our vibe labels were created with the use of OpenAI's ChatGPT-4o-mini model. 
To run this portion of code, and OpenAI account is required, which requires a small fee in order to use their model. 
We were able to complete our development for less than $5.00. The labels are also made available in `song_vibes_top_25.csv`.




