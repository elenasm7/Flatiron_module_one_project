#!pip install spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json

playlist_uri = 'spotify:user:spotify:playlist:37i9dQZF1DX82tVoNhkbcO'


def get_token_and_spotify(client_id, client_secret):
    credentials = oauth2.SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)

    token = credentials.get_access_token()
    spotify_token = spotipy.Spotify(auth=token)
    
    return spotify_token

def get_artist_from_playlist(spotify_token, playlist_uri):

    uri = playlist_uri
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    results = spotify_token.user_playlist(username, playlist_id)
    
    l = []              
    for i in results['tracks']['items']:
        l.append((i['track']['artists'][0]['name'],i['track']['artists'][0]['uri']))                     
    return l

def get_artists_attributes(spotify_token,artists_name_and_url):
    import time
    list_dictionary = []
    for artist in artists_name_and_url:
        dict_artists = {}
        urn = str(artist[1])
        results = spotify_token.artist(urn)
        dict_artists['name'] = results['name']
        dict_artists['followers'] = results['followers']['total']
        dict_artists['popularity'] = results['popularity']
        dict_artists['genres'] = results['genres']
        dict_artists['urn'] = urn
        list_dictionary.append(dict_artists)
        time.sleep(2)
    return list_dictionary

def get_artist_top_songs(spotify_token, artists_name_and_url):
    import time
    
    list_dictionary = []
    for artist in artists_name_and_url:
        dict_songs = {}
        #dict_songs['uri'] = str(artist[1])
        dict_songs['artist_name'] = str(artist[0])
        dict_songs['uri'] = []
        dict_songs['track_name'] = []
        dict_songs['popularity'] = []
        urn = str(artist[1])
        response = spotify_token.artist_top_tracks(urn)
        for track in response['tracks']:
            tracks = {}
            #dict_songs['track_name'] = track['name']
            dict_songs['uri'].append(track['uri'])
            dict_songs['track_name'].append(track['name'])
            dict_songs['popularity'].append(track['popularity'])
        list_dictionary.append(dict_songs)
        time.sleep(1)
    return list_dictionary

def get_song_features_artists(spotify_token,artists_top_songs):
    import time 
    
    arists_song_features = []
    for i in artists_top_songs:
        artist = {}
        artist['artist_name'] = i['artist_name']
        artist['song_names'] = i['track_name']
        artist['popularity'] = i['popularity']
        artist['acousticness'] = []
        artist['danceability'] = []
        artist['duration_ms'] = []
        artist['energy'] = []
        artist['instrumentalness'] = []
        artist['key'] = []
        artist['liveness'] = []
        artist['loudness'] = []
        artist['mode'] = []
        artist['speechiness'] = []
        artist['tempo'] = []
        artist['time_signature'] = []
        artist['valence'] = []
        for song in range(10):
            uri = i['uri'][song]
            features = spotify_token.audio_features(uri)
            for feature in features:
                test_2 = json.dumps(feature, indent=4)
                testing = test_2.split('\n')
                testing_2 = [s.strip().replace('"', '').replace(',', '').split(': ') for s in testing if s not in ['{','}']]
                dict_test = dict(testing_2)
                artist['acousticness'].append(dict_test['acousticness'])
                artist['danceability'].append(dict_test['danceability'])
                artist['duration_ms'].append(dict_test['duration_ms'])
                artist['energy'].append(dict_test['energy'])
                artist['instrumentalness'].append(dict_test['instrumentalness'])
                artist['key'].append(dict_test['key']) 
                artist['liveness'].append(dict_test['liveness']) 
                artist['loudness'].append(dict_test['loudness']) 
                artist['mode'].append(dict_test['mode']) 
                artist['speechiness'].append(dict_test['speechiness']) 
                artist['tempo'].append(dict_test['tempo']) 
                artist['time_signature'].append(dict_test['time_signature'])
                artist['valence'].append(dict_test['valence'])
                time.sleep(1)
        arists_song_features.append(artist)
    return arists_song_features

