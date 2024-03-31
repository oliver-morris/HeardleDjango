import os
import json
import string
import urllib

class Artist:
    def __init__(self, artist_name, artist_id, spotify):
        if artist_name is None:
            artist_name, artist_id = "Taylor Swift", "06HL4z0CvFAxyc27GXpf02"
        self.artist_name = artist_name
        self.artist_id = artist_id
        self.spotify = spotify
        self.tracks = self.getTracks()

    def getLyrics(self):
        file_name = self.artist_name + " " + self.artist_id
        translator = str.maketrans(string.punctuation, '_'*len(string.punctuation))
        file_name = file_name.translate(translator)
        file_name = file_name.replace(" ", "_")
        abs_path = os.path.abspath(os.path.dirname(__file__))
        lyrics_path = abs_path + "\\lyrics\\" + file_name
        try:
            with open(f"{lyrics_path}.txt", "r", encoding="utf-8") as f:
                file = f.read()
            lyrics_dict = json.loads(file)
        except FileNotFoundError:
            return None
        return lyrics_dict[self.artist_id]["tracks"]

    def setLyrics(self):
        self.spotify.saveLyrics(self.artist_name)
        return self.getLyrics()

    def getTracks(self):
        tracks = []
        file_name = self.artist_name + " " + self.artist_id
        translator = str.maketrans(string.punctuation, '_'*len(string.punctuation))
        file_name = file_name.translate(translator)
        file_name = file_name.replace(" ", "_")
        abs_path = os.path.abspath(os.path.dirname(__file__))
        file_path = abs_path + "\\static\\audios\\" + file_name + "\\tracks.txt"
        try:
            with open(file_path, "r") as f:
                file = f.read()
            file = file.replace("’", "'")
            file = file.replace("â€™", "'")
            tracks = file.split("\n")
            if tracks[0] == "":
                print("YES")
                fail = int("s")
        except:
            _, tracks = self.spotify.getArtistTracks(self.artist_name)
            tracks = list(tracks.values())
            self.tracks = tracks
            self.uploadTracks()
        return tracks

    def uploadTracks(self):
        file_name = self.artist_name + " " + self.artist_id
        translator = str.maketrans(string.punctuation, '_'*len(string.punctuation))
        file_name = file_name.translate(translator)
        file_name = file_name.replace(" ", "_")
        abs_path = os.path.abspath(os.path.dirname(__file__))
        file_path = abs_path + "\\static\\audios\\" + file_name + "\\tracks.txt"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for track in self.tracks:
                    f.write(track + "\n")
        except:
            pass