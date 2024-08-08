from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.permissions import  AllowAny
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from rest_framework import status
from django.contrib.auth import login, logout
from django.conf import settings
from django.views.decorators.cache import cache_page   # @cache_page(CACHE_TTL) über def
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.

class VideoView(APIView):
    #authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny] # Keine Authentifizierung erforderlich
    serializer_class = VideoSerializer          
    queryset = Video.objects.all()

    def get(self, request, pk=None, format=None):
        if pk:
            video = get_object_or_404(Video, pk=pk)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        
        else:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)

class VideoFileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, quality, format=None):
        video = get_object_or_404(Video, pk=pk)
        video_file = None

        if quality == '480p':
            video_file = video.video_480p
        elif quality == '720p':
            video_file = video.video_720p
        elif quality == '1080p':
            video_file = video.video_1080p

        if not video_file:
            raise Http404("Video file not found")

        return FileResponse(video_file.open(), content_type='video/mp4')