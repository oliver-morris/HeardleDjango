from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.utils.safestring import SafeString
import json

from .maintenance import fixFiles
from .Heardle import Heardle
from .Spotify import Spotify


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
    context = {
        'artist': artist_name,
        'song': answer,
        'clips': clips,
        'tracks': tracks,
    }
    context = json.dumps(context)
    if "Taylor_Swift_06HL4z0CvFAxyc27GXpf02" in clips[0]:
        return render(request, "heardle/heardle_people/swiftle.html", {'data': SafeString(context)})
    elif "Ed_Sheeran_6eUKZXaKkcviH0Ku9w2n3V" in clips[0]:
        return render(request, "heardle/heardle_people/ed_sheeran.html", {'data': SafeString(context)})
    elif "Noah_Kahan_2RQXRUsr4IW1f3mKyKsy4B" in clips[0]:
        return render(request, "heardle/heardle_people/noah_kahan.html", {'data': SafeString(context)})
    else:
        return render(request, "heardle/homepage.html")
    #return render(request, "heardle/heardle.html", {'data': SafeString(context)})

def homepage(request):
    return render(request, "heardle/homepage.html")


