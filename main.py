import os

from spotify_playlists import PublicPlaylist
import reddit

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials



def main():
    playlist = PublicPlaylist()
    playlist.add_songs()

    
