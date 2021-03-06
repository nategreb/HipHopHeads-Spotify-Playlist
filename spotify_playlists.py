import os

import reddit

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


#query string example: "track:Dyno artist:Jay Critch"

#client doesn't access user information. endpoints with authorization can't be accesed
client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())  #read read.me


class PublicPlaylist:
    user = os.environ["SPOTIFY_USER"] #replace with your username
    playlist_id = os.environ["PLAYLIST_ID"] #replace with the playlist id you want. You can also use the below methods to set it
    scope = "playlist-modify-public" #spotify has different authorization scopes
    
    
    user_authorization = spotipy.Spotify(oauth_manager=SpotifyOAuth(scope=scope, username=user)) #read read.me 
    

    #returns track ID. else, NoneType.
    def get_id(self, query):
        result = client.search(q=query, type="track", limit=1, market="US")
        if len(result) > 0 and len(result['tracks']['items']) > 0:
            return result['tracks']['items'][0]['id']


    #creates a playlist given a name and description    
    def create_playlist(self, name, description):
        self.user_authorization.user_playlist_create(user=self.user, name=name, public=True, 
                            collaborative=None, description=description)


    #returns the playlist ID: String
    #optional 'name' argument. Returns current id if name is null or not found.
    def get_playlist_id(self, **kwargs):
        if len(kwargs) > 0:
            playlists = self.user_authorization.user_playlists(self.user)
            for playlist in playlists['items']:  
                if playlist['name'] == kwargs['name']:  
                    return playlist['id']
        return self.playlist_id 

    
    #set the playlist_id based on name of playlist
    def set_playlist_id(self, name):
        self.playlist_id = self.get_playlist_id(name=name)


    #returns query format given track name
    def format_song(self, track):
        track = track.split('-')
        if len(track) == 2:            
            #title[1] is the song name
            #title[0] is the artist                                  
            return self.get_id(f"track:{track[1].strip()} artist:{track[0].strip()})")
        return None


    #adds songs to playlist based on the freshest r/hiphopheads post
    #need to include SPOTIFY's RATE LIMITING
    def add_songs(self, get_songs):
        ids = []
        posts = get_songs()
        with open('current_songs.txt', 'w') as file:
            for title in posts:        
                #spotify has max       
                if len(ids) > 100:
                    break
                song_id = self.format_song(track=title)
                if song_id is not None:                    
                    ids.append(song_id)    
                    file.write(f"{song_id}\n")
        self.user_authorization.user_playlist_add_tracks(self.user, self.playlist_id, ids, position=None) 

    
    #adds just the songs from the hottest posts
    def add_hot_songs(self):
        self.add_songs(reddit.get_hottest_posts)
    

    #adds the songs from the hottest posts with the Fresh tag
    #tags have limited use, unfortunately...
    def add_fresh_songs(self):
        self.add_songs(reddit.get_latest_fresh_posts)



    #removes songs from playlist
    def clear_playlist(self):                  
       with open("current_songs.txt", "r+") as curr_songs:      
            self.user_authorization.user_playlist_remove_all_occurrences_of_tracks(self.user, 
                                                                                   self.playlist_id, 
                                                                                   curr_songs.read().splitlines()) 
            curr_songs.truncate(0)

        
#Private playlists need a different authorization scope 
class PrivatePlaylist(PublicPlaylist):
    scope = "playlist-modify-private"
    def create_playlist(self, name, description):
        self.user_authorization.user_playlist_create(user=self.user, name=name, public=False, 
                                                    collaborative=None, description=description)



#get the HIT rate of number of querys with matching spotify IDs from total FRESH posts 
def hit_rate():
    id = []
    playlist = PublicPlaylist()
    posts = reddit.get_latest_fresh_posts()
    for title in posts:               
        song_id = playlist.format_song(track=title)
        if song_id is not None:
            id.append(song_id)
    print(float(len(id))/float(len(posts)))