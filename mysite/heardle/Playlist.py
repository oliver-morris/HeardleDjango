import os
import json
import string
import urllib

class Playlist:
    def __init__(self, spotify, playlist_url):
        self.playlist_url = playlist_url
        self.playlist_id = playlist_url.split("/playlist/")[1]
        self.spotify = spotify
        self.playlist_name, self.tracks = self.getTracks()

    def getTracks(self):
        tracks = []
        playlist_name, tracks = self.spotify.getPlaylistTracks(self.playlist_id)
        tracks = list(tracks.values())
        return playlist_name, tracks
