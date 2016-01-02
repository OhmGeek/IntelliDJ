import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cID = "clientID"
cSecret = "secretID"
credManager = SpotifyClientCredentials(client_id = cID,client_secret =cSecret)
spotify = spotipy.Spotify(client_credentials_manager = credManager)
l = spotify.user_playlist_tracks("USER ID",playlist_id="PLID", fields = 'items(track(id))',limit = 100)
print l
