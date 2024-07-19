from django.shortcuts import render, get_object_or_404, redirect
from httplib2 import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework import status, generics
from django.contrib.auth import login, logout, authenticate, get_user_model
from email.mime.image import MIMEImage
from videoflix.settings import MEDIA_URL
from .models import CustomUser
from .serializers import CustomUserSerializer
from .forms import RegistrationForm
import os
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponseRedirect
from django.utils.html import mark_safe
# Create your views here.


# Sends Email to activate user
def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = "Confirm your email"
    logo_path = os.path.join(settings.BASE_DIR, 'templates', 'users', 'logo.png')
    logo_cid = 'logo_cid'
    message = render_to_string("users/verify_email.html", {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        'logo_cid': logo_cid
    })
    to_email = user.email
    email = EmailMultiAlternatives(subject=mail_subject, body="", to=[to_email])
    email.attach_alternative(mark_safe(message), "text/html")
    with open(logo_path, 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', f'<{logo_cid}>')
        mime_image.add_header('Content-Disposition', 'inline')
        email.attach(mime_image)
    email.send()
    

# Sends Email to requesting user to reset password
def reset_password(user, request):
    current_site = get_current_site(request)
    mail_subject = "Reset your Password"
    logo_path = os.path.join(settings.BASE_DIR, 'templates', 'users', 'logo.png')
    logo_cid = 'logo_cid'
    message = render_to_string("users/reset_password.html", {
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        'logo_cid': logo_cid
    })
    to_email = user.email
    email = EmailMultiAlternatives(subject=mail_subject, body="", to=[to_email])
    email.attach_alternative(mark_safe(message), "text/html")
    with open(logo_path, 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', f'<{logo_cid}>')
        mime_image.add_header('Content-Disposition', 'inline')
        email.attach(mime_image)
    email.send()

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
    
class RegisterUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            send_activation_email(user, request)
            return Response({'message': 'Registration successful. Activation email sent.'})  # Oder eine andere URL
        else:
            return Response({'message': 'could not send an email'})

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                reset_password(user, request)
                return Response({'message': 'Reset email sent.'})  # Oder eine andere URL
            except CustomUser.DoesNotExist:
                return Response({'message': 'User not found.'})
        else:
            return Response({'message': 'could not send an email'})
    

def activate_user(request, uidb64, token):
        # CustomUser = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            
            login(request, user)
            messages.success(request, "Your account has been successfully activated!")
            # return HttpResponseRedirect('angular seite wenn sie online ist')
            return HttpResponseRedirect('http://localhost:4200/')# angular eingeloggt zu videos oder so
        else:
            messages.error(request, "Activation link is invalid or expired")
            return HttpResponseRedirect('http://localhost:4200/login')
            
            


        
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204) 