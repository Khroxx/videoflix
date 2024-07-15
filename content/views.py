from django.shortcuts import render
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

    def get(self, request, format=None):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)