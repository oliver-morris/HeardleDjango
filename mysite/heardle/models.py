from django.db import models

class DailySong(models.Model):
    artist_name = models.CharField(max_length=100)
    artist_id = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    date = models.DateField()
    clip1 = models.FileField(upload_to="video/%y")
    clip2 = models.FileField(upload_to="video/%y")
    clip3 = models.FileField(upload_to="video/%y")
    clip4 = models.FileField(upload_to="video/%y")
    clip5 = models.FileField(upload_to="video/%y")
    clip6 = models.FileField(upload_to="video/%y")
    



