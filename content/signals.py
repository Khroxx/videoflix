from content.tasks import *
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Sends variables to tasks.py to format through RQ Worker
    """
    print('video gespeichert')
    if created:
        print('new video created')
        queue = django_rq.get_queue('default', autocommit=True)
        # queue.enqueue(process_video, instance.video_file.path, instance.id)
        queue.enqueue(convert480p, instance.video_file.path, instance.id)
        queue.enqueue(convert720p, instance.video_file.path, instance.id)
        queue.enqueue(convert1080p, instance.video_file.path, instance.id)



@receiver(post_delete, sender=Video)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from database when Video is deleted
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
