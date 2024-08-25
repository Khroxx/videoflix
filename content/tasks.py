import os
import signal
import subprocess
from django.conf import settings
from content.models import Video


def rerun_converter(cmd):
    """
    Runs the ffmpeg command and restarts if terminated by SIGKILL.
    """
    while True:
        process = subprocess.run(cmd)
        if process.returncode == -signal.SIGKILL:
            print("Process terminated by SIGKILL, restarting...")
        else:
            break

    
    
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
    
    
# HLS converting

def convert_to_hls(source, video_id):
    """
    Converts source file to HLS with multiple quality levels and saves files in corresponding folder.
    """
    base_name = os.path.join(settings.MEDIA_ROOT, 'hls', os.path.basename(source).rsplit('.', 1)[0])
    os.makedirs(base_name, exist_ok=True)
    
    qualities = {
        '1080p': ('1920x1080', '5000k'),
        '720p': ('1280x720', '2800k'),
        '480p': ('854x480', '1400k')
    }
    
    for quality, (resolution, bitrate) in qualities.items():
        cmd = [
            'ffmpeg',
            '-i', source,
            '-preset', 'fast',
            '-g', '48',
            '-sc_threshold', '0',
            '-map', '0:v',
            '-map', '0:a?',
            '-s:v', resolution,
            '-c:v', 'libx264',
            '-b:v', bitrate,
            '-c:a', 'aac',
            '-strict', '-2',
            '-f', 'hls',
            '-hls_time', '10',
            '-hls_playlist_type', 'vod',
            '-hls_segment_filename', f'{base_name}/{quality}_%03d.ts',
            f'{base_name}/{quality}.m3u8'
        ]
        
        rerun_converter(cmd)
    
    master_playlist = os.path.join(base_name, 'master.m3u8')
    with open(master_playlist, 'w') as f:
        f.write('#EXTM3U\n')
        for quality in qualities.keys():
            f.write(f'#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION={qualities[quality][0]}\n')
            f.write(f'{quality}.m3u8\n')
    
    video = Video.objects.get(id=video_id)
    video.hls_playlist = os.path.relpath(master_playlist, settings.MEDIA_ROOT)
    video.save()
    
    if os.path.exists(source):
        os.remove(source)