from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework import status
from django.contrib.auth import login, logout
from .models import CustomUser
from .serializers import CustomUserSerializer

# Create your views here.

class CustomUserView(APIView):
    permission_classes = [AllowAny] 
    
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return Response({"message": "erfolgreich gelöscht"})
    
    
class RegisterUserView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        
        user = CustomUser.objects.get(username=username)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username
            })
        else:
            return Response({"error": "Falsche Anmeldedaten"}, status=400)
        
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204) 