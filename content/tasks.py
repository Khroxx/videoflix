import os
import subprocess
from django.conf import settings
from content.models import Video


def convert480p(source, video_id):
    """
    Converts source file to 480p and saves file in corresponding folder
    """
    base_name = os.path.join(settings.MEDIA_ROOT, '480p', os.path.basename(source).rsplit('.', 1)[0])
    target = f"{base_name}_480p.mp4"
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]
    subprocess.run(cmd, capture_output=True)
    
    video = Video.objects.get(id=video_id)
    video.video_480p.name = os.path.relpath(target, settings.MEDIA_ROOT)
    video.save()


def convert720p(source, video_id):
    """
    Converts source file to 720p and saves file in corresponding folder
    """
    base_name = os.path.join(settings.MEDIA_ROOT, '720p', os.path.basename(source).rsplit('.', 1)[0])
    target = f"{base_name}_720p.mp4"
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd720',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]
    subprocess.run(cmd)
    
    video = Video.objects.get(id=video_id)
    video.video_720p.name = os.path.relpath(target, settings.MEDIA_ROOT)
    video.save()


def convert1080p(source, video_id):
    """
    Converts source file to 1080p and saves file in corresponding folder and deletes original source file
    """
    base_name = os.path.join(settings.MEDIA_ROOT, '1080p', os.path.basename(source).rsplit('.', 1)[0])
    target = f"{base_name}_1080p.mp4"
    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd1080',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2', 
        target
    ]
    subprocess.run(cmd, check=True)
    
    video = Video.objects.get(id=video_id)
    video.video_1080p.name = os.path.relpath(target, settings.MEDIA_ROOT)
    video.save()
    if os.path.exists(source):
        os.remove(source)
    
    
def exportJson():
    shell = [
        'python', 'manage.py', 'shell'
    ]
    imp = [
        'from', 'core.admin', 'import', 'VideoResource'
    ]
    data = [
        'dataset', '=', 'VideoResource().export()'
    ]
    action = [
        'print(dataset.json)'
        'dataset.json', '>', 'exportJson.txt'
    ]
    subprocess.run(shell)
    subprocess.run(imp)
    subprocess.run(data)
    subprocess.run(action)
    