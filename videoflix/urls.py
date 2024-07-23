from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from content.views import VideoView
from users.views import *


def redirect_to_admin(request):
    return redirect('/admin/')

urlpatterns = [
    # path('', redirect_to_admin),
    path('admin/', admin.site.urls),
    path('videos/', VideoView.as_view()),
    path('__debug__/', include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('user/verify/', send_activation_email, name='verify_email'),
    # path('user/reset_password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('send_reset_email/', SendResetEmailView.as_view(), name='reset_email'),
    path('get-csrf-token/', get_csrf_token, name="csrf_token"),
    # path('user/send-reset-password/<str:uidb64>/<str:token>/', confirm_reset_password, name='confirm_reset'),
    path('user/register/', RegisterUserView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_user, name="activate"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', CustomUserView.as_view()),
    path('users/<str:uidb64>/', CustomUserView.as_view(), name='user-update'),
    path('users/<str:uidb64>/delete/', CustomUserView.as_view(), name='delete_user'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
