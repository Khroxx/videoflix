from datetime import date
from django.db import models


class Video(models.Model):
    categories = [
        ('New on Videoflix', 'New on Videoflix'),
        ('Dcoumentary', 'Documentary'),
        ('Drama', 'Drama'),
        ('Romance', 'Romance')
    ]
    
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    category = models.CharField(max_length=50, choices=categories, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True, null=True)
    hls_playlist = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title