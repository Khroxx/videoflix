from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
# from django.contrib.auth import get_user_model

# Create your tests here.


class UserAccountTests(TestCase):
        
    # register user
    def test_registration(self):
        response = self.client.post(reverse('register'), data={
            'email': 'test@test.de',
            'username': 'bari',
            'password': 'rkjpk123'
        })
        self.assertTrue(CustomUser.objects.filter(email='test@test.de').exists())
        print("User wurde erfolgreich registriert")
        
    
    # register and login
    def test_login(self):
        response = self.client.post(reverse('register'), data={
            'email': 'test@test.de',
            'username': 'bari',
            'password': 'rkjpk123'
        })
        
        self.client.post(reverse('login'), data={
            'email': 'test@test.de',
            'password': 'rkjpk123'
        })
        print("User loggt ein")
        
        login_response = self.client.post(reverse('login'), data={
            'email': 'test@test.de',
            'password': 'rkjpk123'
        })
        print("User wurde korrekt eingeloggt")