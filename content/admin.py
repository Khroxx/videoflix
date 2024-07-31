from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    # resource_class = VideoResource
    pass


# admin.site.register(VideoAdmin) # Fällt weg weil da oben @admin.register
# admin.site.register(Video)