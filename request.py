import sys
import spotipy
import spotipy.util as util
import json
import csv

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
    name = "Radiohead"
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        print artist['name'], artist['images'][0]['url']
    uri = 'spotify:user:spotify:playlist:37i9dQZEVXcBUQYDbHABNI'
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
    results = sp.user_playlist(username, playlist_id)
    
    ofile  = open('Test.csv', "wb")
    writer = csv.writer(ofile, quotechar='"', quoting=csv.QUOTE_ALL)
    print json.dumps(results['tracks']['items'][0], indent=4)
    writer.writerow([
    	"Track Name",
    	"Album Name",
    	"Track Number"
    ])
    for track in results['tracks']['items']:
    	writer.writerow([
    		track['track']['name'], 
    		track['track']['album']['name'],
    		track['track']['track_number']
    	])
    ofile.close()
	
else:
    print "Can't get token for", username
