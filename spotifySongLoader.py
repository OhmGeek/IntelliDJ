import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
class SpotifyLoader(object):
	"""docstring for SpotifyLoader"""
	def __init__(self, clientID,clientSecret):
		cred_manager = SpotifyClientCredentials(client_id = clientID, client_secret = clientSecret)
		self.spotify = spotipy.Spotify(client_credentials_manager = cred_manager)

	def get_playlist_track_list(self, userID, playlistID,lim = 100):
		data = self.spotify.user_playlist_tracks(userID, playlist_id = playlistID, fields = 'items(track(id))',limit = lim)
		data = data['items'] #get rid of other items. Store as a list
		return_data = []
		for item in data:
			return_data.append(item['track']['id'])
		return return_data
		
	def add_tracks_to_playlist(self,userID,playlistID,tracks):
		self.spotify.user_playlist_add_tracks(userID,playlistID,tracks)
