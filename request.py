import sys
import spotipy
import spotipy.util as util
import csv
from get_lyrics import sentiment

albums = set()

# create a csv file and write headers to it
ofile = open('Test6.csv', "wb")
writer = csv.writer(ofile, quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow([
    "Track Name",
    "Album Name",
    "Album Release Date",
    "Total Tracks on Album",
    "Popularity",
    "Artists",
    "Duration (ms)",
    "Track Number",
    "Sentiment",
    "Key",
    "Mode",
    "Time Signature",
    "Acousticness",
    "Danceability",
    "Energy",
    "Instrumentalness",
    "Liveness",
    "Loudness",
    "Speechiness",
    "Valence",
    "Tempo"
])

# write songs from playlist to csv
def print_playlist(sp, playlist):
    # get playlists in a category
    results = sp.category_playlists(playlist)
    items = results['playlists']['items']
    
    # loop through playlists in a category
    for item in items:
        # owner of playlist
        owner = item['owner']['display_name']
        # id of playlist
        id = item['id']
        # tracks in playlist
        tracks = sp.user_playlist_tracks(owner, id)['items']
        
        # loop through tracks
        for track in tracks:
            try:
                # get only albums that have not been seen before
                if track['track']['album']['album_type'] == "album" and track['track']['album']['id'] not in albums:
                    # get all tracks on album
                    album_tracks = sp.album_tracks(track['track']['album']['id'])['items']
                    
                    # loop through tracks on album
                    for album_track in album_tracks:
                        # get version of track that has more features available
                        t = sp.track(album_track['uri'])
                        # get audio features of track
                        audioFeatures = sp.audio_features([album_track['uri']])
                        # get artists for track
                        artists = ""
                        try:
                            for artist in t['artists']:
                                artists = artists + artist['name'].encode('utf-8') + ','
                            # write features to csv
                            writer.writerow([
                                t['name'].encode('utf-8'),
                                t['album']['name'].encode('utf-8'),
                                t['album']['release_date'],
                                t['album']['total_tracks'],
                                t['popularity'],
                                artists,
                                t['duration_ms'],
                                t['track_number'],
                                sentiment(t['name'].encode('utf-8'), t['artists'][0]['name'].encode('utf-8')),
                                audioFeatures[0]['key'],
                                audioFeatures[0]['mode'],
                                audioFeatures[0]['time_signature'],
                                audioFeatures[0]['acousticness'],
                                audioFeatures[0]['danceability'],
                                audioFeatures[0]['energy'],
                                audioFeatures[0]['instrumentalness'],
                                audioFeatures[0]['liveness'],
                                audioFeatures[0]['loudness'],
                                audioFeatures[0]['speechiness'],
                                audioFeatures[0]['valence'],
                                audioFeatures[0]['tempo']
                            ])
                        except UnicodeDecodeError:
                            print "Unicode Decode Error"
                            pass
                    # add album id to albums
                    albums.add(track['track']['album']['id'])
            except TypeError:
                pass

scope = 'user-library-read'
client_id = '7c9b11cd0657484a91f87d8dd67fb70d'
client_secret = '246e3b84aff7420c9e4cf4ed44a7080e'
redirect_uri = 'http://localhost:8889/callback'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

# api token
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    # create instance of spotify
    sp = spotipy.Spotify(auth=token)
    # call print playlist on country category
    print_playlist(sp, "country")
else:
    print "Can't get token for", username

ofile.close()
