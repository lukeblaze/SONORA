from django.db import models

class Song(models.Model):
    song_name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    emotion = models.CharField(max_length=50)  # E.g., happy, sad, calm, etc.

    def __str__(self):
        return f"{self.song_name} by {self.artist} ({self.emotion})"
