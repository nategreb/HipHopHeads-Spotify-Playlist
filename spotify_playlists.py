import os

import reddit

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


#query string example: "track:Dyno artist:Jay Critch"


class PublicPlaylist:
    user = os.environ["SPOTIFY_USER"]
    playlist_id = os.environ["PLAYLIST_ID"]
    scope = "playlist-modify-public"
    client = spotipy.Spotify(auth_manager=SpotifyClientCredentials()) #doesn't access user information. endpoints with authorization can't be accesed
    user_authorization = spotipy.Spotify(oauth_manager=SpotifyOAuth(scope=scope, username=user)) #username


    #returns track ID. else, NoneType.
    def get_id(self, query):
        result = self.client.search(q=query, type="track", limit=1, market="US")
        if len(result) > 0 and len(result['tracks']['items']) > 0:
            return result['tracks']['items'][0]['id']


    def create_playlist(self, name, description):
        self.user_authorization.user_playlist_create(user=self.user, name=name, public=True, 
                            collaborative=None, description=description)


    #returns the playlist ID: String
    def get_playlist_id(self, playlist_name):
        playlists = user_authorization.user_playlists(user)
        for playlist in playlists['items']:  # iterate through playlists I follow
            if playlist['name'] == playlist_name:  # filter for newly created playlist
                return playlist['name']
        return None

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
        id = []
        posts = get_songs()
        for title in posts:        
            #spotify has max       
            if len(id) > 100:
                break
            song_id = self.format_song(track=title)
            if song_id is not None:
                print(f"{song_id} was added")
                id.append(song_id)
        self.user_authorization.user_playlist_add_tracks(self.user, self.playlist_id, id, position=None) 

    
    #adds just the songs from the hottest posts
    def add_hot_songs(self):
        self.add_songs(reddit.get_hottest_posts)
    

    #adds the songs from the hottest posts with the Fresh tag
    #tags have limited use, unfortunately...
    def add_fresh_songs(self):
        self.add_songs(reddit.get_latest_fresh_posts)


    #reverse of adding freshest songs
    def remove_fresh_songs(self):
        self.clear_playlist(reddit.get_latest_fresh_posts)

    
    #reverse of adding hottest songs
    def remove_hot_songs(self):
        self.clear_playlist(reddit.get_hottest_posts)
    

    #same methodology of add_songs but removes all occurences at the end. 
    #assuming reddit.getId is kept constant with query limit, 
    def clear_playlist(self, get_songs):           
        id = []
        posts = get_songs()
        for title in posts:
            song_id = self.format_song(track=title)
            if song_id is not None:
                print(f"{song_id} was remove")
                id.append(song_id)
        self.user_authorization.user_playlist_remove_all_occurrences_of_tracks(self.user, self.playlist_id, id)  

        
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
