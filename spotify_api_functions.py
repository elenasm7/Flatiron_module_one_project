#!pip install spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import time

female_playlist_uri = 'spotify:user:spotify:playlist:37i9dQZF1DX82tVoNhkbcO'
male_playlist_uri = 'spotify:user:spotify:playlist:37i9dQZF1DWSsIr3Vjy37l'

def get_token_and_spotify(client_id, client_secret):
    '''
    Here we pass our spotify client id and client secret, this returns an 
    authentification token to send requests to the spotify api with the 
    following functions.
    '''
    credentials = oauth2.SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)

    token = credentials.get_access_token()
    spotify_token = spotipy.Spotify(auth=token)
    
    return spotify_token

def get_artist_from_playlist(spotify_token, playlist_uri):
    '''
        This function takes a playlist uri (link) and returns all of the artists in the playlist. It then 
        returns a list of the artist's name and the uri to their page.
    '''

    uri = playlist_uri
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    results = spotify_token.user_playlist(username, playlist_id)
    
    l = []              
    for i in results['tracks']['items']:
        l.append((i['track']['artists'][0]['name'],i['track']['artists'][0]['uri']))                     
    return l

def get_artists_attributes(spotify_token,artists_name_and_url):
    '''
    this takes the artists names and uris returned from the previous function get_artist_from_playlist()
    and returns attributes about each artist, including: followers count, genres, uri, and artist popularity.
    Returns a pandas Data Frame of all attributes, each artist represneted as a row.
    '''
    list_dictionary = []
    for artist in artists_name_and_url:
        dict_artists = {}
        urn = str(artist[1])
        results = spotify_token.artist(urn)
        dict_artists['name'] = results['name']
        dict_artists['followers'] = results['followers']['total']
        dict_artists['artist_popularity'] = results['popularity']
        dict_artists['genres'] = results['genres']
        dict_artists['urn'] = urn
        list_dictionary.append(dict_artists)
    return list_dictionary

def get_artist_top_songs(spotify_token, artists_name_and_url):
    '''
    this function takes the artist name and uri, uses the spotipy library and returns a list 
    of the artists top songs. It then creates a dataframe with each row representing an artist.
    '''
    
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
    return list_dictionary

def get_song_features_artists(spotify_token,artists_top_songs):
    
    '''
    this function uses spotipy and the spotify api to return the audio attributes of each song
    by our top artists, and then creates a brand new data frame--each row corresponding to a song.
    Each top artist only has ten (or less) top songs, which was gathered from our last function: 
    get_artist_top_songs()
    '''
    
    arists_song_features = []
    for i in artists_top_songs:
        artist = {}
        artist['artist_name'] = i['artist_name']
        artist['song_names'] = i['track_name']
        artist['song_popularity'] = i['popularity']
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
        for song in range(len(i['uri'])):
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
        arists_song_features.append(artist)
    return arists_song_features

def mean_of_artist_columns_to_df(artists,song_df): 
    '''
    this function takes the artists file created before with attributes such as followers and popularity,
    and concatinates it with a new data frame of the mean audio features of each song by the artists 
    '''
    values = []
    for i in artists:
        the_mean = song_df[song_df['artist_name'] == i].mean()
        values.append(np.append(i, the_mean.values))
    column_name = np.append('artist_name', the_mean.index)
    return pd.DataFrame(values, columns=column_name)

def create_subplots_songFeatures(dataFrame,column_names,png_name):   
    '''
    Function to create sub-regplots from a given DataFrame and specified 
    columns. You pass the DataFrame, the list of column names, and the name
    of the png file it will be saved as.
    '''
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, wspace=0.2)
    col_len = len(column_names)
    nrows = (col_len//3)+1
    for i in range(1, col_len):
        ax = fig.add_subplot(nrows, 3, i)
        #plt.figure(figsize=(10,3))
        #ax.text(0.5, 0.5, str((4, 3, i)), fontsize=18, ha='center')
        sns.regplot(x='song_popularity', y=column_names[i], data= dataFrame).set_title(f'song_popularity vs {column_names[i]}')
        fig.set_size_inches(35.5, 25.5)
        fig.subplots_adjust(hspace=0.2)
    fig.savefig(png_name)
    plt.show()
