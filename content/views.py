import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from rest_framework.authtoken.views import  APIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(csrf_protect, name='dispatch')
class VideoView(APIView):
    permission_classes = [AllowAny]
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
        
    def post(self, request, *args, **kwargs):
        # Dummy POST method
        return Response({"message": "POST request received"})
        