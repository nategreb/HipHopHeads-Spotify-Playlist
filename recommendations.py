from spotify_playlists import PrivatePlaylist, client


#a list of recommended track ids based on artists 
#up to 5 seeds for artists, genres, tracks can be provided
#at least one of each is required
#@param: artists, genres, tracks: String[]
def get_recommended_tracks(artists, genres, tracks):
    if not artists or not genres or not tracks:
        print("at least one of artists, genres, and tracks are required")
    else:
        artists = seed_artists(artists)
        tracks = seed_tracks(tracks)
        if artists and tracks and genres:
            ids = []
            for track in client.recommendations(seed_artists=artists, seed_genres=genres, seed_tracks=tracks)['tracks']:
                ids.append(track['id'])
            return ids
        else: 
            print("No ids were found for artists and/or tracks")
    return None 


def seed_artists(artists):
    ids = []
    artists = artists[:5]
    for i in range(len(artists)):
        id = get_id(artists[i], 'artist')
        if id is not None:
            ids.append(id)
    return ids


def seed_tracks(tracks):
    ids = []
    tracks = tracks[:5]
    for i in range(len(tracks)):        
        id = get_id(tracks[i], 'track')
        if id is not None:
            ids.append(id)
    return ids

#helper function for getting an id 
#(query: String, kind: String)
#kind is the seed type 
def get_id(query, kind):    
    result = client.search(q=f"{kind}:{query}", type=kind, limit=1)
    if len(result) > 0 and len(result[kind+'s']['items']) > 0:
        return result[kind+'s']['items'][0]['id']
    return None
