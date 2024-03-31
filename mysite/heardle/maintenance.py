import os

def fixFiles():
    directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/audios')
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isdir(f):
            if filename == "custom":
                for file in os.listdir(f):
                    f2 = os.path.join(f, file)
                    if os.path.isfile(f2+"\\full_audio.mp4"):
                        try:
                            os.remove(f2+"\\full_audio.mp4")
                            os.remove(f2+"\\full_audio2.mp4")
                        except:
                            pass
            else:
                if os.path.isfile(f+"\\full_audio.mp4"):
                    try:
                        os.remove(f+"\\full_audio.mp4")
                        os.remove(f+"\\full_audio2.mp4")
                    except:
                        pass