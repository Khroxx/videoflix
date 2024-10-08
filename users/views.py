from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework import status, generics
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import login, logout, authenticate
from email.mime.image import MIMEImage
from videoflix.settings import MEDIA_URL
from .models import CustomUser
from .serializers import CustomUserSerializer, ResetEmailSerializer
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.html import mark_safe
from django.middleware.csrf import get_token

# Create your views here.


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
    
    
class ResendActivationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    send_activation_email(user, request)
                    return Response({'message': 'Activation email resent.'}, status=200)
                else:
                    return Response({'message': 'User is already active.'}, status=200)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User not found.'}, status=404)
        else:
            return Response({'message': 'Email not provided.'}, status=400)
        
        
def reset_password(email, request):
    current_site = get_current_site(request)
    mail_subject = "Reset your Password"
    logo_path = os.path.join(settings.BASE_DIR, 'templates', 'users', 'logo.png')
    logo_cid = 'logo_cid'
    csrf_token = get_csrf_token(request)
    user = CustomUser.objects.get(email=email)
    message = render_to_string("users/reset_password.html", {
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'logo_cid': logo_cid,
        'csrf_token': csrf_token
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


class SendResetEmailView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetEmailSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                reset_password(email, request)
                return Response({"success": "E-Mail zum Zurücksetzen des Passworts gesendet."}, status=HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "Benutzer mit dieser E-Mail-Adresse existiert nicht."}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CustomUserView(APIView):
    permission_classes = [AllowAny] 
    
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def put(self, request, uidb64, format=None):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user.set_password(serializer.validated_data.get("password"))
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self, request, uidb64, format=None):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)
        user.delete()
        return Response({"message": "erfolgreich gelöscht"})
    
    
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        username = serializer.validated_data['email'].split('@')[0]
        user = authenticate(request, username=username,  password=password)
        if user is not None:
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
                return Response({'message': 'Reset email sent.'})
            except CustomUser.DoesNotExist:
                return Response({'message': 'User not found.'})
        else:
            return Response({'message': 'could not send an email'})
    

def activate_user(request, uidb64, token):
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
            return HttpResponseRedirect('http://localhost:4200/welcome/login?activated=true')# angular eingeloggt zu videos oder so
        else:
            messages.error(request, "Activation link is invalid or expired")
            return HttpResponseRedirect('http://localhost:4200/welcome/login?activated=false')            


        
class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204) 
    
    
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})