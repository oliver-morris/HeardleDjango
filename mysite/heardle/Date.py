import time
import os
from datetime import datetime

class Date:
    def __init__(self, filename):
        utc_time = time.time()
        self.filename = filename
        self.date_int = int(datetime.fromtimestamp(utc_time).strftime("%Y%m%d"))
        self.set_date, self.song = self.getDate(filename)

    def getDate(self, artist_id):
        path = self.getPath(f"{self.filename}/date.txt")
        print(path)
        try:
            with open(path, "r") as f:
                file = f.read()
            file = file.split("\n")
        except:
            file = [0, None]
        if file == [""]:
            file = [0, None]
        date = file[0]
        song = file[1]
        if not song:
            return [0, None]
        return int(date), song

    def getFiles(self):
        mypath = os.path.abspath(os.path.dirname(__file__))
        mypath = "static\\audios\\" + self.filename
        files = []
        for i in range(6):
            files.append(mypath+f"\\clip{str(i+1)}.mp4")
        return files

    def getPath(self, file_path):
        abs_path = os.path.abspath(os.path.dirname(__file__))
        return abs_path + "\\static\\audios\\" + file_path.replace("/", "\\")

    def makeFile(self, song):
        path = self.getPath(f"{self.filename}/date.txt")
        message = str(self.date_int) + "\n"
        message += str(song)
        with open(path, "w") as f:
            f.write(message)

