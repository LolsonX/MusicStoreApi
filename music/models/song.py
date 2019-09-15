from django.db import models

from music.models.artist import Artist


class Song(models.Model):
    title = models.CharField(max_length=255)
    #duration = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

