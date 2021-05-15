import os
import time

from spotify_playlists import PublicPlaylist

playlist = PublicPlaylist()

#main script for HipHopHeads playlist
def main():
    while(1):
        playlist.add_hot_songs()
        time.sleep(604800)
        playlist.clear_playlist()
                

if __name__ == "__main__":
    main()


    
