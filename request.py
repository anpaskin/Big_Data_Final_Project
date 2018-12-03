import sys
import spotipy
import spotipy.util as util
import csv
import json

ofile = open('Test2.csv', "wb")
writer = csv.writer(ofile, quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow([
    "Track Name",
    "Album Release Date",
    "Total Tracks on Album",
    "Popularity",
    "Artists",
    "Duration (ms)",
    "Track Number",
    "Key",
    "Mode",
    "Time Signature",
    "Acousticness",
    "Danceability",
    "Energy",
    "Instrumentalness",
    "Liveness",
    "Speechiness",
    "Valence",
    "Tempo"
])

def print_playlist(sp, playlist):
    results = sp.category_playlists(playlist)

    items = results['playlists']['items']
    for item in items:
        owner = item['owner']['display_name']
        id = item['id']
        tracks = sp.user_playlist_tracks(owner, id)['items']
        
        for track in tracks:
            try:
                if track['track']['album']['album_type'] == "album":
                    album_tracks = sp.album_tracks(track['track']['album']['id'])['items']
                    for album_track in album_tracks:
                        t = sp.track(album_track['uri'])
                        audioFeatures = sp.audio_features([album_track['uri']])
                        artists = ""
                        for artist in t['artists']:
                            artists = artists + artist['name'].encode('utf-8') + ','
                        writer.writerow([
                            t['name'].encode('utf-8'),
                            t['album']['release_date'],
                            t['album']['total_tracks'],
                            t['popularity'],
                            artists,
                            t['duration_ms'],
                            t['track_number'],
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
            except TypeError:
                print "TypeError"
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

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    print_playlist(sp, "toplists")
    print_playlist(sp, "pop")
else:
    print "Can't get token for", username

ofile.close()
