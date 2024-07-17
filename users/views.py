from django.shortcuts import render, get_object_or_404, redirect
from httplib2 import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework import status, generics
from django.contrib.auth import login, logout, authenticate, get_user_model
from .models import CustomUser
from .serializers import CustomUserSerializer
from .forms import RegistrationForm
from django.core.mail import EmailMultiAlternatives
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponseRedirect

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
            # Send activation email
            current_site = get_current_site(request)
            mail_subject = "Confirm your email"
            message = render_to_string("users/verify_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            
            # to_email = serializer.validated_data.get("email")
            to_email = user.email
            email = EmailMultiAlternatives(subject=mail_subject, body="", to=[to_email])
            # email.content_subtype = "html"
            email.attach_alternative(message, "text/html")
            email.send()
            return Response({"poggers": "es ging?"})  # Oder eine andere URL
             # return HttpResponseRedirect('http://localhost:4200/')  # Oder eine andere URL
        else:
            return HttpResponseRedirect('http://localhost:4200/register')  # Oder eine andere URL bei Fehler
    
    # def register_user(request):
    #     form = RegistrationForm()
    #     if request.method == "POST":
    #         form = RegistrationForm(request.POST)
    #         if form.is_vaid():
    #             user = form.save(commit=False)
    #             user.is_active = False
    #             user.save()
            
    #             current_site = get_current_site(request)
    #             mail_subject = "Confirm your email"
    #             message = render_to_string("users/verify_email.html",{
    #                 "user": user,
    #                 "domain": current_site.domain,
    #                 "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    #                 "token": account_activation_token.make_token(user)
    #             })
    #             to_email = form.cleaned_data.get("email")
    #             email = EmailMessage(
    #                 mail_subject, message, to=[to_email]
    #             )
    #             email.send()
    #             messages.success(request, "Please check your email to complete the registration.")
    #             # return HttpResponseRedirect('angular seite wenn sie online ist')
    #             return HttpResponseRedirect('http://localhost:4200/') # angular login?
    #     # return render(request, "register.html", {"form": form})
    #     return HttpResponseRedirect('http://localhost:4200/register')
    #     # return HttpResponseRedirect('https://bari-sopa.com/projects/videoflix/register')
                            
    

def activate_user(request, uidb64, token):
        CustomUser = get_user_model()
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