from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from content.views import VideoView

def redirect_to_admin(request):
    return redirect('/admin/')

urlpatterns = [
    # path('', redirect_to_admin),
    path('admin/', admin.site.urls),
    path('videos/', VideoView.as_view())

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
