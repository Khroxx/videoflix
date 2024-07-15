from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from content.views import VideoView
from users.views import CustomUserView, RegisterUserView, LoginView, LogoutView


def redirect_to_admin(request):
    return redirect('/admin/')

urlpatterns = [
    # path('', redirect_to_admin),
    path('admin/', admin.site.urls),
    path('videos/', VideoView.as_view()),
    path('__debug__/', include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', CustomUserView.as_view()),
    path('users/<int:pk>/', CustomUserView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', CustomUserView.as_view(), name='delete_user'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
