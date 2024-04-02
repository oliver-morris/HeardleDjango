import string
import random
import difflib
import urllib
import requests
import os
import time
import math
from moviepy import editor
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube
from .Artist import Artist
from .Date import Date
import moviepy.video.io.ImageSequenceClip

class Heardle:
    def __init__(self, spotify, artist_name, custom_id=None, song=None):
        self.spotify = spotify
        self.file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/audios')

        if not custom_id:
            artist_id, artist_name = self.spotify.getArtist(artist_name)
            self.artist_id = artist_id
            self.artist_name = artist_name
            self.file_name = self.setFilename(artist_id, artist_name)
            self.date = Date(self.file_name)
            self.artist = Artist(artist_name, artist_id, spotify)
            if self.checkDate():
                return
        else:
            self.file_name = "/custom/" + custom_id + "/"
        if not song:
            self.song = self.pickSong()
        else:
            self.song = song
        self.clip_length = 1
        self.song_video = self.downloadSong()
        self.clips = self.getClips()
        if not custom_id:
            self.date.makeFile(self.song)

    def checkDate(self):
        if self.date.set_date >= self.date.date_int:
            self.song = self.date.song
            self.clips = self.date.getFiles()
            return True
        return False

    def pickSong(self):
        try:
            tracks = self.artist.tracks
        except:
            tracks = self.getCustomTracks()
        return (random.choice(tracks).replace("â€™", "'")).replace("’", "'")

    def setFilename(self, artist_id, artist_name):
        file_name = artist_name + " " + artist_id
        translator = str.maketrans(string.punctuation, '_'*len(string.punctuation))
        file_name = file_name.translate(translator)
        file_name = file_name.replace(" ", "_")
        return file_name

    def downloadSong(self):
        if "/custom/" not in self.file_name:
            artist_name_string = self.artist.artist_name
            answer = self.song
            youtube_search_query = artist_name_string + " " + answer + " lyric video"
        else:
            youtube_search_query = self.song + " lyric video"
        youtube_search_query = urllib.parse.quote(youtube_search_query)

        youtube_search_endpoint = f"https://www.youtube.com/results?search_query={youtube_search_query}"
        request = requests.get(youtube_search_endpoint)
        status = request.status_code
        if status == 200:
            response = request.text
            video_id = response.split('{"videoRenderer":{"videoId":"')[1]
            video_id = video_id.split('"')[0]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(video_url)
            #try:
            yt = YouTube(video_url)
            #except:
                #print("Connection Error")
            file_name = self.file_name

            yt.streams.filter(progressive=True,
                                  file_extension="mp4").first().download(
                    output_path=f"{self.file_path}/{file_name}",
                    filename="full_audio.mp4")
            return f"{self.file_path}/{file_name}" + "full_audio.mp4"


    def cutClip(self):
        audio_path = f"{self.file_path}/{self.file_name}/full_audio.mp4"
        clip = editor.AudioFileClip(audio_path)
        if clip.duration < 60 + 7 * self.clip_length:
            print("Video not long enough!")
            return
        start = random.randint(30, math.floor(clip.duration - 30 - (7*self.clip_length)))
        end = start + 7*self.clip_length
        audio_path_2 = f"{self.file_path}/{self.file_name}/full_audio2.mp4"
        ffmpeg_extract_subclip(audio_path, start, end, targetname=audio_path_2)
        return audio_path_2

    def getClips(self):
        audio_path = self.cutClip()
        duration = 7*self.clip_length
        clips = []
        for i in range(6):
            end = (i+1) * self.clip_length
            print(self.file_name)
            clip_path = f"/{self.file_name}/clip{str(i+1)}.mp4"
            ffmpeg_extract_subclip(audio_path, 0, end, targetname=self.file_path+clip_path)
            clips.append(clip_path)
        return clips


        # loading video dsa gfg intro video
        clip = editor.VideoFileClip(video_path)

        # getting only first 5 seconds
        clip = clip.subclip(0, end)

        # loading audio file
        audioclip = editor.AudioFileClip(audio_path).subclip(0, end)

        # adding audio to the video clip
        videoclip = clip.set_audio(audioclip)

        # showing video clip
        videoclip.write_videofile(final_path, temp_audiofile=video_path)

    def getCustomTracks(self):
        with open(f"{self.file_path}/{self.file_name}tracks.txt", "r") as f:
            file = f.read()
        return file.split("\n")


