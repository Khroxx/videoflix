from datetime import date
from django.db import models

# Create your models here.

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_480p = models.FileField(upload_to='480p',blank=True, null=True)
    video_720p = models.FileField(upload_to='720p', blank=True, null=True)
    video_1080p = models.FileField(upload_to='1080p', blank=True, null=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True, null=True)

    def __str__(self):
        return self.title