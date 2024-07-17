from django.contrib import admin
from .models import CustomUser
from .forms import RegistrationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = RegistrationForm
    fieldsets = (
                    ('Individuelle Daten',
                        {'fields': (
                            'custom',
                            'phone',
                            'address',
                            )
                        }
                    ),
                    *UserAdmin.fieldsets, 
                )

# admin.site.register(CustomUser)