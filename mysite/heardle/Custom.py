from .Playlist import Playlist
from .Artist import Artist
import os

class Custom:
    def __init__(self, spotify, user_input):
        self.spotify = spotify
        self.artist = None
        self.custom_id = os.urandom(16).hex()
        if "spotify.com/playlist/" in user_input:
            self.playlist_url = user_input
            self.playlist = Playlist(spotify, user_input)
            self.tracks = self.playlist.tracks
            self.upload()
        else:
            artist_id, artist_name = self.spotify.getArtist(user_input)
            self.artist = Artist(artist_name, artist_id, spotify)
            self.tracks = self.artist.tracks
            self.upload()


    def getDetails(self):
        if self.artist:
            return self.artist.artist_name, self.artist.tracks
        else:
            return self.playlist.playlist_name, self.playlist.tracks

    def upload(self):
        abs_path = os.path.abspath(os.path.dirname(__file__))
        abs_path += "\\static\\audios\\custom\\" + self.custom_id
        file_path = abs_path + "\\tracks.txt"
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        if os.path.isfile(abs_path):
            #create a new id    (loop until free)
            #add if need more files
            pass
        with open(file_path, "w", encoding="utf-8") as f:
            for track in self.tracks:
                f.write(track + "\n")