import subprocess


def convert480p(source):
    base_name = source.rsplit('.', 1)[0]
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


def convert720p(source):
    base_name = source.rsplit('.', 1)[0]
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


def convert1080p(source):
    base_name = source.rsplit('.', 1)[0]
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
    subprocess.run(cmd)