# HipHopHeads-Spotify-Playlist

The core of this project is to scrape the subreddit called "HipHopHeads" and create a playlist from it. Essentially, every four days, the script will clear the "HipHopHeads" Spotify playlist, scrape r/HipHopHeads from the latest hot posts, and then add them to the playlist. Other features for personal usage will be mentioned below. 

To replicate it, you must:
  1. Create a Reddit API app 
  2. Create a Spotify API app
  
For spotify_playlists.py and Spotify API: 
  In spotify_playlists.py, you will see the member variables "client" and "user_authorization". For these, you need to declare and instantiate variables as        
  SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI in the file. If you plan to keep the code as is, just declare and instantiate them as environment 
  variables. 
  
For reddit.py and Reddit API:
  This module is more hard coded and directly intended for r/HipHopHeads. As seen in the file, either create environment variables as depicted, or instantiate them       
  directly. The general format for scraping this subreddit is by taking the titles of the posts which, for the most part, are in the format "[AUTHOR] - [SONG]". 
  Overall, requesting the Reddit API with larger limits is pretty slow.
  

