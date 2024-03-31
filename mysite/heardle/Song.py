import lyricsgenius
import urllib
import re

class Song:
    def __init__(self, title, artist, id=None):
        self.song_title = title
        self.artist_name = artist
        self.song_id = id
        self.lyrics, self.lyrics_encoded = self.getLyrics()


    def getLyrics(self):
        client_secret = "oyIsecGjwILvsxQjitL_ZygXUyVJ4Jl34veXfW7nnBb2fKvM7g-fxIno7xAZ6KO147ZifmCVh0-06OHFu3IHSg"
        genius = lyricsgenius.Genius(client_secret)
        song = genius.search_song(self.song_title, self.artist_name)
        lyrics = song.lyrics
        lyrics = lyrics.replace("\u2005", " ")
        lyrics = lyrics.split("\n")
        lyric_array = []
        lyric_array_encoded = []
        for lyric in lyrics:
            if "[" in lyric and "]" in lyric or lyric == "":
                pass
            elif re.search("[0-999] Contributor", lyric[:16]):
                return None, None
            else:
                match = re.search("[0-999]?K?Embed", lyric)
                if match:
                    lyric = lyric[:match.start()]
                lyric2 = urllib.parse.quote(lyric)
                lyric_array.append(lyric)
                lyric_array_encoded.append(lyric2)
        return lyric_array, lyric_array_encoded