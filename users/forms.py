from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    # password = forms.CharField(label='Password')
    email = forms.EmailField(required=True)
    
    class Meta:        
        model = CustomUser        
        fields = ['email', 'password']
        
        def clean(self, *args, **kwargs):
            email = self.cleaned_data.get('email')
            # password = self.cleaned_data.get('password')
            email_check = CustomUser.objects.filter(email=email)
            if email_check.exists():
                raise forms.ValidationError('This Email already exists')
            return email
            