from datetime import date
from django.db import models

# Create your models here.

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_480p = models.URLField(max_length=1024, default='', blank=True, null=True)
    video_720p = models.URLField(max_length=1024, default='', blank=True, null=True)
    video_1080p = models.URLField(max_length=1024, default='', blank=True, null=True)
    category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title