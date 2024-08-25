import os
import tempfile
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .tasks import convert_to_hls
from .models import Video
from django.core.files.uploadedfile import SimpleUploadedFile



class VideoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.video_file_path = os.path.join(self.temp_dir.name, "test_video.mp4")
        with open(self.video_file_path, 'wb') as f:
            f.write(b"file_content")
        
        self.video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        self.video = Video.objects.create(title="Test Video", description="Test Description", video_file=self.video_file)

    def test_get_single_video(self):
        response = self.client.post(reverse('single-video', kwargs={'pk': self.video.pk}), data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("get single video test passed")

    def test_get_all_videos(self):
        response = self.client.get(reverse('videos'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        video_count = Video.objects.count()
        self.assertEqual(len(response.data), video_count)
        self.assertEqual(response.data[0]['title'], self.video.title)
        print("get all videos Test passed")
        
    def test_convert_to_hls(self):
        # Call the convert_to_hls function
        convert_to_hls(self.video_file_path, self.video.id)
        
        # Verify that the HLS playlist and segments are created
        hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls')
        hls_test_video = os.path.join(hls_dir, 'test_video')
        print(f"Checking if HLS directory exists at: {hls_test_video}")
        self.assertTrue(os.path.exists(hls_test_video))
        

        master_playlist = os.path.join(hls_test_video, 'master.m3u8')
        print(f"Checking if master playlist exists at: {master_playlist}")
        self.assertTrue(os.path.exists(master_playlist))
        
        print("HLS conversion test passed")