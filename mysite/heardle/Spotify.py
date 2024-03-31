import requests
import json
import urllib
import string
import os
from .Song import Song

class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.auth()
        self.header = {
            "Authorization": f"Bearer  {self.access_token}"
        }

    def auth(self):
        #authenticate spotify account
        token_endpoint = "https://accounts.spotify.com/api/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        request = requests.post(token_endpoint, headers=header, data=body)
        status = request.status_code
        response = request.json()
        access_token = response["access_token"]
        return access_token

    def getArtist(self, artist_name):
        #returns the artist id and their name
        artist_name = urllib.parse.quote(artist_name)
        endpoint = "https://api.spotify.com/v1/search"
        url = f"{endpoint}?q={artist_name}&type=artist"
        request = requests.get(url, headers=self.header)
        status = request.status_code
        if status == 200:
            response = request.json()
        else:
            return None, None
        id = response["artists"]["items"][0]["id"]
        name = response["artists"]["items"][0]["name"]
        return id, name

    def getAlbums(self, artist_id):
        albums_endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        request = requests.get(albums_endpoint, headers=self.header)
        status = request.status_code
        if status == 200:
            response = request.json()
        else:
            print(request.text)
            return
        albums = {}
        for album in response["items"]:
            albums[album["id"]] = album["name"]
        return albums

    def getTracks(self, album_id=None, playlist_id=None):
        #spotify error does not respond with last track of an album!!!
        if album_id:
            url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
            request = requests.get(url, headers=self.header)
            status = request.status_code
            if status == 200:
                response = request.json()
                tracks = {}
                for track in response["items"]:
                    tracks[track["id"]] = track["name"].replace("â€™", "'")
                return tracks
            print(status)
            print(request.text_content)
            print("No album found!")
        else:
            url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
            request = requests.get(url, headers=self.header)
            response = request.json()
            status = request.status_code
            if status == 200:
                response = request.json()
                tracks = {}
                for track in response["tracks"]["items"]:
                    tracks[track["track"]["id"]] = track["track"]["name"]
                return tracks
            print("No playlist found!")

    def getArtistTracks(self, artist_name):
        artist_id, artist_name = self.getArtist(artist_name)
        albums = self.getAlbums(artist_id)
        tracks = {}
        for album_id in list(albums.keys()):
            tracks.update(self.getTracks(album_id=album_id))
        return artist_id, self.fixTracks(tracks)

    def fixTracks(self, tracks):
        new_tracks = {}
        for id in list(tracks.keys()):
            name = tracks[id]
            name = name.split(" -")[0]
            name = name.split(" (")[0]
            name = name.split("/")[0]
            name = name.replace("â€™", "'")
            if name not in list(new_tracks.values()) and name:
                new_tracks[id] = name
        return new_tracks


    def saveLyrics(self, artist_name):
        print("Finding Tracks...")
        artist_id, tracks = self.getArtistTracks(artist_name)
        print("Tracks Found\nStarting Save...")
        lyrics_dict = {artist_id: {'name': artist_name, 'tracks': []}}
        count = 1
        for name in list(tracks.values()):
            print(f"Track ({str(count)}/{str(len(list(tracks.values())))})")
            count += 1
            song = Song(name, artist_name)
            lyrics = song.lyrics_encoded
            if lyrics:
                name = urllib.parse.quote(name)
                lyrics_dict[artist_id]["tracks"].append([name, lyrics])

        file_name = artist_name + " " + artist_id
        translator = str.maketrans(string.punctuation, '_'*len(string.punctuation))
        file_name = file_name.translate(translator)
        file_name = file_name.replace(" ", "_")
        lyrics_dict = str(lyrics_dict)
        lyrics_dict = lyrics_dict.replace("'", '"')
        abs_path = os.path.abspath(os.path.dirname(__file__))
        file_name = abs_path + "\\lyrics\\" + file_name
        with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
            f.write(lyrics_dict)
        f.close()
        print("Lyrics have been uploaded")

    def findSong(self, user_input, artist_name):
        endpoint = "https://api.spotify.com/v1/search"
        user_input = urllib.parse.quote(user_input)
        artist_name = urllib.parse.quote(artist_name)
        url = endpoint + f"?q={user_input}%20track:{user_input}%20artist:{artist_name}&type=track"
        request = requests.get(url, headers=self.header)
        status = request.status_code
        if status == 200:
            response = request.json()
        else:
            return None, None
        id = response["tracks"]["items"][0]["id"]
        name = response["tracks"]["items"][0]["name"]
        return id, name

    def getPlaylistTracks(self, playlist_id):
        playlist_tracks_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        request = requests.get(playlist_tracks_endpoint, headers=self.header)
        status = request.status_code
        if status == 200:
            response = request.json()
        else:
            print(f"This Playlist is private so tracks cannot be viewed")
            raise KeyError

        playlist_name = response["name"]
        response = response["tracks"]
        tracks = {}
        artists = {}
        for track in response["items"]:
            track_name = track["track"]["name"].replace("â€™", "'")
            track_id = track["track"]["id"]
            artist_name = track["track"]["album"]["artists"][0]["name"]
            tracks[track_id] = track_name
            artists[track_id] = artist_name
        tracks = self.fixTracks(tracks)
        tracks2 = {}
        for track_id in (tracks.keys()):
            tracks2[track_id] = tracks[track_id] + " - " + artists[track_id]
        return playlist_name, tracks2


