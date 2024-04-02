from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.utils.safestring import SafeString
from django.conf import settings
import json

from .maintenance import fixFiles
from .Heardle import Heardle
from .Spotify import Spotify

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
spotify = Spotify(client_id, client_secret)

def heardle(request):
    artist_name = request.GET.get('artist', '')
    print(artist_name)
    if artist_name:
        h = Heardle(spotify, artist_name)
        if not h.song:
            artist_name = "Taylor Swift"#h.artist_name
            answer = "All Too Well"#h.song
            clips = []#h.clips
            tracks = []#h.artist.tracks
        else:
            artist_name = h.artist_name
            answer = h.song
            clips = h.clips
            tracks = h.artist.tracks
    else:
        custom_id = args.get("customid")
        song = args.get("song")
        h = Heardle(spotify, "_", custom_id, song)
        answer = h.song
        clips = h.clips
        tracks = h.getCustomTracks()
    fixFiles()
    clips2 = []
    for clip in clips:
        if "static" not in clip:
            clips2.append("static/audios" + clip)
        else:
            break
    if clips2:
        clips = clips2
    context = {
        'artist': artist_name,
        'song': answer,
        'clips': clips,
        'tracks': tracks,
    }
    context = json.dumps(context)
    print(clips)
    return render(request, "heardle/heardle.html", {'data': SafeString(context)})

def homepage(request):
    return render(request, "heardle/homepage.html")


